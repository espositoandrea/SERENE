export class ScreenCoordinates {
    public x: number;
    public y: number;

    public set(x: number, y: number): void {
        this.x = x || 0;
        this.y = y || 0;
    }

    constructor(x?: number, y?: number) {
        this.x = x || 0;
        this.y = y || 0;
    }
}

export type RawData = {
    image: string | undefined; ///< The webcam snapshot as a data URI.
    timestamp: number; ///< The timestamp
    url: string; ///< The visited URL
    mouse: { ///< Various data regarding the mouse
        position: ScreenCoordinates; ///< The mouse position. p[0] is the X position, p[1] is the Y position.
        buttons: Array<number>; ///< The mouse buttons (as integer codes)
    };
    scroll: { ///< Various data about the scroll position
        absolute: ScreenCoordinates; ///< The absolute scroll position. a[0] is the X position, a[1] is the Y position.
        relative: ScreenCoordinates; ///< The relative scroll position (from the bottom of the screen). r[0] is the X position, r[1] is the Y position.
    };
    window: ScreenCoordinates; ///< Various data about the browser's window. w[0] is the width, w[1] is the height.
    keyboard: Array<string>; ///< An array of keys that's currently pressed
}

export type MessageEvents = {
    readonly "data-collected": RawData;
    readonly "surveycompleted": { userId: string };
    readonly "webcampermission": null;
    readonly "browserfocuschange": { inFocus: boolean };
    readonly "enabledisableextension": { enabled: boolean };
    readonly "snapwebcam": string;
    readonly "stopwebcampermission": null;
}

export class Message<T extends keyof MessageEvents>{
    public event: T;
    public data: MessageEvents[T];

    constructor(event: T, data?: MessageEvents[T]) {
        this.event = event;
        this.data = data || null;
    }
}


export namespace KeyboardKey {
    export enum Types {
        ALPHABETIC,
        NUMERIC,
        SYMBOLIC,
        FUNCTION
    }

    // eslint-disable-next-line: no-inner-declarations
    export function getType(key: string): Types {
        //Remove all accents and diactritics
        key = key.toString().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

        // The following 'if's will fail if the key's length not equal to 1
        if (/^[a-zA-Z]$/i.test(key)) {
            return Types.ALPHABETIC;
        }
        else if (/^[0-9]$/.test(key)) {
            return Types.NUMERIC;
        }
        else if (/^[|\\!"£$%&/()=?^'-_.:,;#@+*[\]]$/.test(key)) {
            return Types.SYMBOLIC;
        }
        else {
            return Types.FUNCTION;
        }
    }
}
