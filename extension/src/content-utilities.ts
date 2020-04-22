import { ScreenCoordinates } from './common-types';

export type RawData = {
    timestamp: number, ///< The timestamp
    url: string, ///< The visited URL
    mouse: { ///< Various data regarding the mouse
        position: ScreenCoordinates, ///< The mouse position. p[0] is the X position, p[1] is the Y position.
        buttons: Set<number> ///< The mouse buttons (as integer codes)
    },
    scroll: { ///< Various data about the scroll position
        absolute: ScreenCoordinates ///< The absolute scroll position. a[0] is the X position, a[1] is the Y position.
        relative: ScreenCoordinates ///< The relative scroll position (from the bottom of the screen). r[0] is the X position, r[1] is the Y position.
    },
    width: ScreenCoordinates, ///< Various data about the browser's window. w[0] is the width, w[1] is the height.
    keyboard: Set<string> ///< An array of keys that's currently pressed
}

export default class ContentScript {
    private static readonly keyboard: RawData['keyboard'] = new Set<string>();
    private static readonly mousePosition: RawData['mouse']['position'] = new ScreenCoordinates();
    private static readonly mouseButtons: RawData['mouse']['buttons'] = new Set<number>();

    private static get relativeScroll(): RawData['scroll']['relative'] {
        const height = document.body.offsetHeight;
        const width = document.body.offsetWidth;

        let absoluteY = window.pageYOffset;
        let absoluteX = window.pageXOffset;

        let relativeY = 100 * (absoluteY + document.documentElement.clientHeight) / height;
        let relativeX = 100 * (absoluteX + document.documentElement.clientWidth) / width;
        return new ScreenCoordinates(relativeX, relativeY);
    }

    public static sendCollectionRequest(event: keyof WindowEventMap) {
        const objectToSend: RawData = {
            keyboard: ContentScript.keyboard,
            mouse: {
                buttons: ContentScript.mouseButtons,
                position: ContentScript.mousePosition
            },
            scroll: {
                absolute: new ScreenCoordinates(window.pageXOffset, window.pageYOffset),
                relative: ContentScript.relativeScroll
            },
            timestamp: Date.now(),
            url: window.location.href,
            width: new ScreenCoordinates(window.innerWidth, window.outerHeight)
        }

        console.log(objectToSend)

        // chrome.runtime.sendMessage({ event: 'data-collected', data: objectToSend });
    }

    public static registerEvents() {
        window.addEventListener('mousedown', (e: MouseEvent) => {
            ContentScript.mouseButtons.add(e.button);
            ContentScript.sendCollectionRequest('mousedown')
        });
        window.addEventListener('mouseup', (e: MouseEvent) => {
            ContentScript.mouseButtons.delete(e.button);
            ContentScript.sendCollectionRequest('mouseup')
        });
        window.addEventListener('mousemove', e => {
            ContentScript.mousePosition.set(e.clientX, e.clientY);
            ContentScript.sendCollectionRequest('mousemove')
        });
        window.addEventListener('keydown', (e: KeyboardEvent) => {
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
                this.relativeScroll.set(window.pageXOffset, window.pageYOffset);
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
