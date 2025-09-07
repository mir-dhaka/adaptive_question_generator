// src/app/utils/ObjectUtils.ts
export class ObjectUtil {
    static removeProperties<T extends object>(obj: T, keys: (keyof T)[]): Partial<T> {
        const newObj = { ...obj };
        keys.forEach((key) => {
            delete newObj[key];
        });
        return newObj;
    }

    static hasProperties<T extends object>(obj: T, keys: (keyof T)[]): boolean {
        return keys.every((key) => key in obj);
    }

    static retainProperties<T extends object>(obj: T, keys: (keyof T)[]): Partial<T> {
        const newObj: Partial<T> = {};
        keys.forEach((key) => {
            if (key in obj) {
                newObj[key] = obj[key];
            }
        });
        return newObj;
    }
    static convertToBase64(obj: any): string {
        // Convert the object to a JSON string
        const jsonString = JSON.stringify(obj);

        // Encode the JSON string to Base64
        const base64String = btoa(jsonString);

        return base64String;
    }
}
