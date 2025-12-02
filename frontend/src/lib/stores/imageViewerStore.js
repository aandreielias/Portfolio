import { writable } from 'svelte/store';

export const imageViewerStore = writable({
    isOpen: false,
    src: '',
    alt: ''
});

export function openImage(src, alt = '') {
    imageViewerStore.set({ isOpen: true, src, alt });
}

export function closeImage() {
    imageViewerStore.set({ isOpen: false, src: '', alt: '' });
}
