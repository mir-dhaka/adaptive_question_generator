export interface RegistrationModel {
    first_name: string;
    last_name: string;
    user_name:string;
    email: string;
    password: string;
    role:string;
}

export interface LoginModel {
    email: string;
    user_name:string;
    password: string;
}

export interface ForgetPasswordModel {
    email: string;
}

export interface ChangePassword {
    currentPassword: string;
    newPassword: string;
}

export interface ResetPasswordModel {
    email: string;
    forgetPasswordKey: string;
    password: string;
}

export interface LoginResponseModel {
    token: string;
    expiry: number;
}
