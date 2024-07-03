import type {
  OpenAPIClient,
  Parameters,
  UnknownParamsObject,
  OperationResponse,
  AxiosRequestConfig,
} from 'openapi-client-axios';

declare namespace Components {
    namespace Schemas {
        /**
         * AddFriend
         */
        export interface AddFriend {
            /**
             * User Id
             */
            user_id: number;
        }
        /**
         * HTTPValidationError
         */
        export interface HTTPValidationError {
            /**
             * Detail
             */
            detail?: /* ValidationError */ ValidationError[];
        }
        /**
         * LoginBody
         */
        export interface LoginBody {
            /**
             * Email
             */
            email: string;
            /**
             * Password
             */
            password: string;
        }
        /**
         * LoginResponse
         */
        export interface LoginResponse {
            /**
             * Session Token
             */
            session_token: string;
            /**
             * Id
             */
            id: number;
            /**
             * Username
             */
            username: string;
        }
        /**
         * Message
         */
        export interface Message {
            /**
             * Id
             */
            id?: number;
            /**
             * Sender
             */
            sender: number;
            /**
             * Reciever
             */
            reciever: number;
            /**
             * Content
             */
            content: string;
            /**
             * Sent At
             */
            sent_at?: string;
        }
        /**
         * RegisterBody
         */
        export interface RegisterBody {
            /**
             * Username
             */
            username: string;
            /**
             * Email
             */
            email: string;
            /**
             * Password
             */
            password: string;
            /**
             * Pincode
             */
            pincode: number;
            /**
             * Topics
             */
            topics: string[];
        }
        /**
         * RegisterUniqueError
         */
        export interface RegisterUniqueError {
            /**
             * Message
             */
            message: string;
            /**
             * Unique Field
             */
            unique_field: /* Unique Field */ ("email") | ("username");
        }
        /**
         * SendMessageBody
         */
        export interface SendMessageBody {
            /**
             * Message
             */
            message: string;
        }
        /**
         * Topic
         */
        export interface Topic {
            /**
             * Id
             */
            id?: number;
            /**
             * Name
             */
            name: string;
        }
        /**
         * UserInformation
         * Same as tables.User but without the password
         */
        export interface UserInformation {
            /**
             * Id
             */
            id: number;
            /**
             * Username
             */
            username: string;
            /**
             * Email
             */
            email: string;
            /**
             * Pincode
             */
            pincode: number;
            /**
             * Name
             */
            name: /* Name */ string | null;
            /**
             * Number
             */
            number: /* Number */ string | null;
            /**
             * Address
             */
            address: /* Address */ string | null;
            /**
             * Joined On
             */
            joined_on: string;
        }
        /**
         * UserWithTopics
         */
        export interface UserWithTopics {
            user: /**
             * UserInformation
             * Same as tables.User but without the password
             */
            UserInformation;
            /**
             * Topics
             */
            topics: /* Topic */ Topic[];
            /**
             * Is Friend
             */
            is_friend: boolean;
        }
        /**
         * ValidationError
         */
        export interface ValidationError {
            /**
             * Location
             */
            loc: (string | number)[];
            /**
             * Message
             */
            msg: string;
            /**
             * Error Type
             */
            type: string;
        }
    }
}
declare namespace Paths {
    namespace AddFriend {
        export interface HeaderParameters {
            authorization: /* Authorization */ Parameters.Authorization;
        }
        namespace Parameters {
            /**
             * Authorization
             */
            export type Authorization = string;
        }
        export type RequestBody = /* AddFriend */ Components.Schemas.AddFriend;
        namespace Responses {
            export type $200 = any;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace GetCurrentUser {
        export interface HeaderParameters {
            authorization: /* Authorization */ Parameters.Authorization;
        }
        namespace Parameters {
            /**
             * Authorization
             */
            export type Authorization = string;
        }
        namespace Responses {
            export type $200 = /**
             * UserInformation
             * Same as tables.User but without the password
             */
            Components.Schemas.UserInformation;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace GetInboxUsers {
        export interface HeaderParameters {
            authorization: /* Authorization */ Parameters.Authorization;
        }
        namespace Parameters {
            /**
             * Authorization
             */
            export type Authorization = string;
        }
        namespace Responses {
            /**
             * Response Get Inbox Users Get Inbox Users  Get
             */
            export type $200 = /* UserWithTopics */ Components.Schemas.UserWithTopics[];
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace GetMessages {
        export interface HeaderParameters {
            authorization: /* Authorization */ Parameters.Authorization;
        }
        namespace Parameters {
            /**
             * Authorization
             */
            export type Authorization = string;
            /**
             * Username
             */
            export type Username = string;
        }
        export interface PathParameters {
            username: /* Username */ Parameters.Username;
        }
        namespace Responses {
            /**
             * Response Get Messages Get Messages  Username  Get
             */
            export type $200 = /* Message */ Components.Schemas.Message[];
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace HomePage {
        namespace Responses {
            export type $200 = any;
        }
    }
    namespace Login {
        export type RequestBody = /* LoginBody */ Components.Schemas.LoginBody;
        namespace Responses {
            export type $200 = /* LoginResponse */ Components.Schemas.LoginResponse;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace Logout {
        export interface HeaderParameters {
            authorization: /* Authorization */ Parameters.Authorization;
        }
        namespace Parameters {
            /**
             * Authorization
             */
            export type Authorization = string;
        }
        namespace Responses {
            export type $200 = any;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace Register {
        export type RequestBody = /* RegisterBody */ Components.Schemas.RegisterBody;
        namespace Responses {
            export type $200 = /* LoginResponse */ Components.Schemas.LoginResponse;
            export type $409 = /* RegisterUniqueError */ Components.Schemas.RegisterUniqueError;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace SelfUserProfile {
        export interface HeaderParameters {
            authorization: /* Authorization */ Parameters.Authorization;
        }
        namespace Parameters {
            /**
             * Authorization
             */
            export type Authorization = string;
        }
        namespace Responses {
            export type $200 = /* UserWithTopics */ Components.Schemas.UserWithTopics;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace SendMessage {
        export interface HeaderParameters {
            authorization: /* Authorization */ Parameters.Authorization;
        }
        namespace Parameters {
            /**
             * Authorization
             */
            export type Authorization = string;
            /**
             * Username
             */
            export type Username = string;
        }
        export interface PathParameters {
            username: /* Username */ Parameters.Username;
        }
        export type RequestBody = /* SendMessageBody */ Components.Schemas.SendMessageBody;
        namespace Responses {
            export type $200 = /* Message */ Components.Schemas.Message;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace Suggestion {
        export interface HeaderParameters {
            authorization: /* Authorization */ Parameters.Authorization;
        }
        namespace Parameters {
            /**
             * Authorization
             */
            export type Authorization = string;
        }
        namespace Responses {
            /**
             * Response Suggestion Suggestion Get
             */
            export type $200 = /* UserWithTopics */ Components.Schemas.UserWithTopics[];
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
    namespace UserProfile {
        export interface HeaderParameters {
            authorization: /* Authorization */ Parameters.Authorization;
        }
        namespace Parameters {
            /**
             * Authorization
             */
            export type Authorization = string;
            /**
             * Username
             */
            export type Username = string;
        }
        export interface PathParameters {
            username: /* Username */ Parameters.Username;
        }
        namespace Responses {
            export type $200 = /* UserWithTopics */ Components.Schemas.UserWithTopics;
            export type $422 = /* HTTPValidationError */ Components.Schemas.HTTPValidationError;
        }
    }
}

export interface OperationMethods {
  /**
   * home_page - Home Page
   */
  'home_page'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.HomePage.Responses.$200>
  /**
   * register - Register
   */
  'register'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: Paths.Register.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.Register.Responses.$200>
  /**
   * login - Login
   */
  'login'(
    parameters?: Parameters<UnknownParamsObject> | null,
    data?: Paths.Login.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.Login.Responses.$200>
  /**
   * get_current_user - Get Current User
   */
  'get_current_user'(
    parameters?: Parameters<Paths.GetCurrentUser.HeaderParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GetCurrentUser.Responses.$200>
  /**
   * logout - Logout
   */
  'logout'(
    parameters?: Parameters<Paths.Logout.HeaderParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.Logout.Responses.$200>
  /**
   * suggestion - Suggestion
   */
  'suggestion'(
    parameters?: Parameters<Paths.Suggestion.HeaderParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.Suggestion.Responses.$200>
  /**
   * user_profile - User Profile
   */
  'user_profile'(
    parameters?: Parameters<Paths.UserProfile.HeaderParameters & Paths.UserProfile.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.UserProfile.Responses.$200>
  /**
   * self_user_profile - Self User Profile
   */
  'self_user_profile'(
    parameters?: Parameters<Paths.SelfUserProfile.HeaderParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.SelfUserProfile.Responses.$200>
  /**
   * add_friend - Add Friend
   */
  'add_friend'(
    parameters?: Parameters<Paths.AddFriend.HeaderParameters> | null,
    data?: Paths.AddFriend.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.AddFriend.Responses.$200>
  /**
   * get_inbox_users - Get Inbox Users
   */
  'get_inbox_users'(
    parameters?: Parameters<Paths.GetInboxUsers.HeaderParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GetInboxUsers.Responses.$200>
  /**
   * send_message - Send Message
   */
  'send_message'(
    parameters?: Parameters<Paths.SendMessage.HeaderParameters & Paths.SendMessage.PathParameters> | null,
    data?: Paths.SendMessage.RequestBody,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.SendMessage.Responses.$200>
  /**
   * get_messages - Get Messages
   */
  'get_messages'(
    parameters?: Parameters<Paths.GetMessages.HeaderParameters & Paths.GetMessages.PathParameters> | null,
    data?: any,
    config?: AxiosRequestConfig  
  ): OperationResponse<Paths.GetMessages.Responses.$200>
}

export interface PathsDictionary {
  ['/']: {
    /**
     * home_page - Home Page
     */
    'get'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.HomePage.Responses.$200>
  }
  ['/register']: {
    /**
     * register - Register
     */
    'post'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: Paths.Register.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.Register.Responses.$200>
  }
  ['/login']: {
    /**
     * login - Login
     */
    'post'(
      parameters?: Parameters<UnknownParamsObject> | null,
      data?: Paths.Login.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.Login.Responses.$200>
  }
  ['/get_current_user/']: {
    /**
     * get_current_user - Get Current User
     */
    'get'(
      parameters?: Parameters<Paths.GetCurrentUser.HeaderParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GetCurrentUser.Responses.$200>
  }
  ['/logout/']: {
    /**
     * logout - Logout
     */
    'post'(
      parameters?: Parameters<Paths.Logout.HeaderParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.Logout.Responses.$200>
  }
  ['/suggestion']: {
    /**
     * suggestion - Suggestion
     */
    'get'(
      parameters?: Parameters<Paths.Suggestion.HeaderParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.Suggestion.Responses.$200>
  }
  ['/user_profile/{username}']: {
    /**
     * user_profile - User Profile
     */
    'get'(
      parameters?: Parameters<Paths.UserProfile.HeaderParameters & Paths.UserProfile.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.UserProfile.Responses.$200>
  }
  ['/user_profile']: {
    /**
     * self_user_profile - Self User Profile
     */
    'get'(
      parameters?: Parameters<Paths.SelfUserProfile.HeaderParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.SelfUserProfile.Responses.$200>
  }
  ['/add_friend/']: {
    /**
     * add_friend - Add Friend
     */
    'post'(
      parameters?: Parameters<Paths.AddFriend.HeaderParameters> | null,
      data?: Paths.AddFriend.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.AddFriend.Responses.$200>
  }
  ['/get_inbox_users/']: {
    /**
     * get_inbox_users - Get Inbox Users
     */
    'get'(
      parameters?: Parameters<Paths.GetInboxUsers.HeaderParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GetInboxUsers.Responses.$200>
  }
  ['/send_message/{username}']: {
    /**
     * send_message - Send Message
     */
    'post'(
      parameters?: Parameters<Paths.SendMessage.HeaderParameters & Paths.SendMessage.PathParameters> | null,
      data?: Paths.SendMessage.RequestBody,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.SendMessage.Responses.$200>
  }
  ['/get_messages/{username}']: {
    /**
     * get_messages - Get Messages
     */
    'get'(
      parameters?: Parameters<Paths.GetMessages.HeaderParameters & Paths.GetMessages.PathParameters> | null,
      data?: any,
      config?: AxiosRequestConfig  
    ): OperationResponse<Paths.GetMessages.Responses.$200>
  }
}

export type Client = OpenAPIClient<OperationMethods, PathsDictionary>

