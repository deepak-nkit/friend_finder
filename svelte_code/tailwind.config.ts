import type { Config } from "tailwindcss";
let colors = require("tailwindcss/colors");

export default {
	content: ["./src/**/*.{html,js,svelte,ts}"],

	daisyui: {
		themes: [
			{
				friend_theme: {
					...require("daisyui/src/theming/themes")["cupcake"],
					// primary: "#afF0ffff"
				},
			},
			"cupcake",
			"emerald",
		],
	},
	theme: {
		extend: {
			colors: {
				neutral: colors.slate,
				positive: colors.green,
				urge: colors.violet,
				warning: colors.yellow,
				info: colors.blue,
				critical: colors.red,
			},
		},
	},

	plugins: [
		require("@tailwindcss/typography"),
		// require("@tailwindcss/forms"),
		// require("a17t"),
		require("daisyui"),
	],
} as Config;
