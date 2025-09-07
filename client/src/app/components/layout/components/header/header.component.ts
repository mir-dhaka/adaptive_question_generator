import { Component, OnInit } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { AuthService } from '../../../../services/auth.service';
import { LocalStorageUtil } from '../../../../utils/localstorageUtil';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
    public pushRightClass: string;
    loggedinUser:any=LocalStorageUtil.getUserInfo(); 
    constructor(private translate: TranslateService, public router: Router, private service: AuthService) {
        this.router.events.subscribe((val) => {
            if (val instanceof NavigationEnd && window.innerWidth <= 992 && this.isToggled()) {
                this.toggleSidebar();
            }
        });
    }

    ngOnInit() {
        this.pushRightClass = 'push-right';
        //this.loggedinUser= LocalStorageUtil.getUserInfo();
    }

    isToggled(): boolean {
        const dom: Element = document.querySelector('body');
        return dom.classList.contains(this.pushRightClass);
    }

    toggleSidebar() {
        const dom: any = document.querySelector('body');
        dom.classList.toggle(this.pushRightClass);
    }

    rltAndLtr() {
        const dom: any = document.querySelector('body');
        dom.classList.toggle('rtl');
    }

    onLoggedout() { 
        this.service.logout({ token: 'logout' }, (res) => {
            if (res.success == true) {
                LocalStorageUtil.clearToken();
            } else {
                alert(res.message);
            }
        });
    }

    changeLang(language: string) {
        this.translate.use(language);
    }
}
