export type RawData = {
    timestamp: number, ///< The timestamp
    url: string, ///< The visited URL
    mouse: { ///< Various data regarding the mouse
        position: [number, number], ///< The mouse position. p[0] is the X position, p[1] is the Y position.
        buttons: { ///< The mouse buttons
            left: boolean, ///< Is the left button pressed?
            middle: boolean, ///< Is the middle button pressed?
            right: boolean ///< Is the right button pressed?
        }
    },
    scroll: { ///< Various data about the scroll position
        absolute: [number, number] ///< The absolute scroll position. a[0] is the X position, a[1] is the Y position.
        relative: [number, number] ///< The relative scroll position (from the bottom of the screen). r[0] is the X position, r[1] is the Y position.
    },
    width: [number, number], ///< Various data about the browser's window. w[0] is the width, w[1] is the height.
    keyboard: string[] ///< An array of keys that's currently pressed
}

export default class ContentScript {
    private static readonly keyboard: Set<string> = new Set<string>();

    public static sendCollectionRequest(event: keyof WindowEventMap) {
        const objectToSend: RawData = {
            keyboard: null,
            mouse: null,
            scroll: null,
            timestamp: Date.now(),
            url: null,
            width: null
        }

        console.log(objectToSend)

        // chrome.runtime.sendMessage({ event: 'data-collected', data: objectToSend });
    }

    public static registerEvents() {
        window.addEventListener('mousedown', (e: MouseEvent) => {
            e.button;
            ContentScript.sendCollectionRequest('mousedown')
        });
        window.addEventListener('mouseup', (e: MouseEvent) => {
            e.button;
            ContentScript.sendCollectionRequest('mouseup')
        });
        window.addEventListener('mousemove', e => {
            let o = { x: e.clientX, y: e.clientY }
            ContentScript.sendCollectionRequest('mousemove')
        });
        window.addEventListener('keydown', (e: KeyboardEvent) => {
            e.key;
            ContentScript.keyboard.add(e.key);
            ContentScript.sendCollectionRequest('keydown')
        });
        window.addEventListener('keyup', (e: KeyboardEvent) => {
            if (!ContentScript.keyboard.delete(e.key)) {
                // Error fix: released a key that was pressed
                // Example: the key '[' emits as '[' on press and 'è' on release on Chrome
                ContentScript.keyboard.clear();
            }
            ContentScript.sendCollectionRequest('keyup')
        });
        window.addEventListener('scroll', (e: UIEvent) => {
            if (e.target == window) {
                ContentScript.sendCollectionRequest('scroll')
            }
        });
        window.addEventListener('resize', (e: UIEvent) => {
            if (e.target == window) {
                ContentScript.sendCollectionRequest('resize')
            }
        });
    }
}
