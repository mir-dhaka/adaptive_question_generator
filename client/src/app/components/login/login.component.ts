import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { routerTransition } from '../router.animations';
import { AuthService } from '../../services/auth.service';
import { ToastComponent } from '../primeng/components/toast/toast.component';
import { LoginModel } from '../../models/auth.models';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
    animations: [routerTransition()]
})
export class LoginComponent implements OnInit {
    @ViewChild(ToastComponent) toast: ToastComponent;
    model: LoginModel = {
        user_name:'',
        email: '',
        password: ''
    };
    constructor(public router: Router, private service: AuthService) {}
    ngOnInit() {}

    onLoggedin() {
        if (this.model.email.trim() == '' || this.model.password.trim() == '') {
            this.toast.showErrorToast('Email and Password are required');
            return;
        }
        this.model.user_name=this.model.email;
        
        this.service.login(this.model, (res) => {
            if (res.success == true) {
                this.toast.showSuccessToast('Login Successful');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else {
                this.toast.showErrorToast(res.message);
            }
        });
    }
}
