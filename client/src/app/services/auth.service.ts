import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Injectable } from '@angular/core';
import { LoginModel, RegistrationModel } from '../models/auth.models';
import { LocalStorageUtil } from '../utils/localstorageUtil';

@Injectable({
    providedIn: 'root'
})
export class AuthService extends BaseService {
    constructor(public http: HttpClient) {
        super('/auth', http, true);
    }
    register(model: RegistrationModel, cb) {
        const url = `${this.apiURL}/register`;
        this.post_by_url(url, model).subscribe((res) => {
            cb(res.body);
        });
    }
    login(model: any, cb) {
        const url = `${this.apiURL}/token`;
        this.post_by_url(url, model).subscribe((res: any) => {
            this.dumpResponseBody(res);
            if (res.body.success == true) { 
                let data={token:res.body.data.token, user_data:res.body.data.user_data};
                LocalStorageUtil.storeLoggedinUserData(data);
            }
            cb(res.body);
        });
    }
    logout(model: any, cb) {
        const url = `${this.apiURL}/logout`;
        this.post_by_url(url, model).subscribe((res: any) => {
            if (res.body.success == true) {
                LocalStorageUtil.clearToken();
            }
            cb(res.body);
        });
    }
    forgetpassword() {}
    resetpassword() {}
}
