import { SvelteMap, SvelteSet } from "svelte/reactivity";
import * as R from "remeda";
import type { Components } from "../../../../backend_openapi";
import { dev } from "$app/environment";
export type Message = Components.Schemas.Message;

type ClientId = string;
type MessageId = number;

/**
   Manager messages for a single chat user.
   Handles polling, sorting, merging etc.
*/
export class ChatManager {
	/**
		Everything is sorted by message_id.
		So newer message are at end
	*/
	initial_messages: Message[] = $state([]);
	polled_messages: Message[] = $state([]);

	// beware that `sent_at` here will be different from the one stored in DB. As this is the time at which the user clicked send.
	// not the time when it got inserted in db.
	pending_messages: SvelteMap<ClientId, { content: string; sent_at: Date }> =
		$state(new SvelteMap());

	latest_known_message_id: MessageId = $state(0);
	known_message_ids: SvelteSet<MessageId> = $state(new SvelteSet());

	pollingAbortController: AbortController;
	pollingPaused: boolean = false;

	constructor(
		initial_messages: Message[],
		public chat_username: string,
	) {
		this.initial_messages = sort_messages(initial_messages);
		this.latest_known_message_id = max_message_id(initial_messages);

		initial_messages.forEach((message) => {
			this.known_message_ids.add(message.id!);
		});

		this.pollingAbortController = new AbortController();
	}

	register_pending_message(content: string, client_id: string) {
		this.pending_messages.set(client_id, { content, sent_at: new Date() });
	}

	register_new_poll(messages: Message[]) {
		/** Stores _only_ messages that we've not seen previously */
		let new_messages: Message[] = [];

		/**
		----------------
		Filter out new messages
		----------------
		*/
		for (const message of messages) {
			const message_id = message.id!;

			/** Ignore if we know the message already */
			if (this.known_message_ids.has(message_id)) {
				continue;
			}

			/**
				Verify we didn't recieve an old message that was previously missed
				If polling works correctly, we should never miss any messages. So if this gets triggered it reflects a bug in code.
			*/
			if (message_id <= this.latest_known_message_id) {
				console.error(`Detected missed message: ${message_id}`);
				if (dev) {
					alert("Missed message. See console.");
				}
			}

			new_messages.push(message);
		}

		/** Return if no new messages */
		if (new_messages.length === 0) {
			return;
		}

		/**
		----------------
		Update the `polled_messages` and other state based on new messages
		----------------
		*/
		new_messages = sort_messages(new_messages);
		this.polled_messages.push(...new_messages.reverse());

		// If we recieved older missed messages, then sorting is messed up.
		// So we need to re-sort it.
		if (new_messages[0].id! <= this.latest_known_message_id) {
			this.polled_messages = sort_messages(this.polled_messages, false);
		}

		this.latest_known_message_id = Math.max(
			max_message_id(new_messages),
			this.latest_known_message_id,
		);

		new_messages.forEach((message) => {
			this.known_message_ids.add(message.id!);
			this.pending_messages.delete(message.client_id);
		});
	}

	async pollMessage(abortSignal: AbortSignal) {
		let response = await fetch(
			`/chat/${this.chat_username}/api/poll_message?after_id=${this.latest_known_message_id}`,
			{
				signal: abortSignal,
			},
		);
		if (!response.ok) {
			console.error(response);
			throw new Error(
				`Unexpected response from server for poll_message: ${response.status}`,
			);
		}
		let data: Components.Schemas.Message[] = await response.json();
		this.register_new_poll(data);
	}

	/**
		Start to poll continously.
		Can optionally provide `condition` which should be function.
		The function will be run after each poll and if the function returns `false`, the polling will be stopped.

		Should only be called once, later use `.pausePolling` and `.resumePolling` to control
	*/
	async initializePolling(condition: () => boolean = () => true) {
		while (condition()) {
			try {
				if (!this.pollingPaused) {
					this.pollingAbortController = new AbortController();
					await this.pollMessage(this.pollingAbortController.signal);
				} else {
					await new Promise((r) => setTimeout(r, 300));
				}
			} catch (e) {
				console.log("polling error: ", e);
				await new Promise((r) => setTimeout(r, 5000));
			}
		}
	}

	pausePolling() {
		this.pollingAbortController.abort();
		this.pollingPaused = true;
	}
	resumePolling() {
		this.pollingPaused = false;
	}
}

function max_message_id(message: Message[], allow_empty: boolean = true) {
	if (!allow_empty && message.length === 0) {
		throw new Error("[max_message_id] Can't find max of empty array");
	}
	return Math.max(...message.map((x) => x.id!), 0);
}

function sort_messages(message: Message[], clone: boolean = true) {
	let cloned = clone ? [...message] : message;
	return cloned.sort((a, b) => a.id! - b.id!);
}
