export namespace loginStatus {
    export { subscribe };
    export function setLogIn(): void;
    export function setLogOut(): void;
}
export const captchaValue: import("svelte/store").Writable<string>;
declare const subscribe: (this: void, run: import("svelte/store").Subscriber<number>, invalidate?: () => void) => import("svelte/store").Unsubscriber;
export {};
