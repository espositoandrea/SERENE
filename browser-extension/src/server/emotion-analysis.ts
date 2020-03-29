export interface Emotions {

}

export default class EmotionAnalysis {
    public static async analyzeImage(dataUri:string){
        return new Promise<Emotions>((resolve, reject) => {
            resolve({})
        });
    }
}