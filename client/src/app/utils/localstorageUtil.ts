// src/app/utils/LocalStorageUtil.ts
export class LocalStorageUtil {
    static token_storate_key: string = 'token';
    static user_login_status_storage_key: string = 'isLoggedin';
    static loggedin_user_data_key: string = "loggedin_user";

    static clearToken(): boolean {
        try {
            localStorage.removeItem(this.token_storate_key);
            localStorage.removeItem(this.user_login_status_storage_key);
            localStorage.removeItem(this.loggedin_user_data_key)
            return true;
        } catch (error) {
            console.error('Error clearing tokens from localStorage:', error);
            return false;
        }
    }
    static getUserInfo():any{
         try {
            let user:any=LocalStorageUtil.get(this.loggedin_user_data_key);
            return user.email; 

        } catch (error) {
            console.error('Error getting user info from localStorage:', error);
            return "No User";
        }

    }

    static storeLoggedinUserData(data: any): boolean {
        try { 
            LocalStorageUtil.store(this.token_storate_key, data.token);
            LocalStorageUtil.store(this.user_login_status_storage_key, true);
            LocalStorageUtil.store(this.loggedin_user_data_key, data.user_data);
            return true;
        } catch (error) {
            console.error('Error saving logged in user data to localStorage:', error);
            return false;
        }
    }
    
    static store(key: string, value: any): void {
        localStorage.setItem(key, JSON.stringify(value));
    }

    static get<T>(key: string): T | null {
        const item = localStorage.getItem(key);
        return item ? (JSON.parse(item) as T) : null;
    }

    static list(): string[] {
        const keys: string[] = [];
        for (let i = 0; i < localStorage.length; i++) {
            keys.push(localStorage.key(i)!);
        }
        return keys;
    }
    static delete(key: string): void {
        localStorage.removeItem(key);
    }
}
