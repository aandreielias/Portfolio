import { writable } from 'svelte/store';

export const projectRegistry = writable([]);
export const activeProject = writable(null);
