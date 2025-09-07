import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { LocalStorageUtil } from '../utils/localstorageUtil';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        // Get the auth token from the service.
        const authToken = this.getAuthToken();
        if (authToken != undefined && authToken.length > 20) {
            // Clone the request and replace the original headers with
            // cloned headers, updated with the authorization.
            const authReq = req.clone({
                headers: req.headers.set('Authorization', `Bearer ${authToken}`)
            });

            // Send cloned request with header to the next handler.
            return next.handle(authReq);
        }
        return next.handle(req);
    }

    private getAuthToken(): string {
        if (LocalStorageUtil.get<Boolean>(LocalStorageUtil.user_login_status_storage_key) == false) {
            return '';
        }

        let tokenData = LocalStorageUtil.get<any>(LocalStorageUtil.token_storate_key);
        return tokenData?.token;
    }
}
