import type { Client as BackendClient } from "./../backend_openapi.js";
import { OpenAPIClientAxios } from "openapi-client-axios";

// TODO(deepak): Change through environment variable
// export const BACKEND_BASE_URL = 'http://server';
export const BACKEND_BASE_URL = "http://localhost:8000";

/*
Run following command to re-generate types (from fastapi openapi.json):
  npx openapicmd typegen http://localhost:8000/openapi.json > src/backend_openapi.d.ts
*/
class BackendAPI {
	api: OpenAPIClientAxios;

	constructor(backend_url: string) {
		this.api = new OpenAPIClientAxios({
			definition: `${backend_url}/openapi.json`,
		});
		this.api.withServer({ url: backend_url, description: "Server" });
		this.api.init<BackendClient>();
	}

	async getClient() {
		console.log("====================== ", this.api.getBaseURL());
		return this.api.getClient<BackendClient>();
	}
}

export const BACKEND_API = new BackendAPI(BACKEND_BASE_URL);
