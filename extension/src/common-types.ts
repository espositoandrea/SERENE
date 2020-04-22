export class ScreenCoordinates {
    public x: number;
    public y: number;

    public set(x: number, y: number) {
        this.x = x || 0;
        this.y = y || 0;
    }

    constructor(x?: number, y?: number) {
        this.x = x || 0;
        this.y = y || 0;
    }
}
