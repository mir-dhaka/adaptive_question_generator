import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BasicDataComponent } from './basicdata.component';
import { CNDListComponent } from '../../primeng/components/list/cndlist';
import { UsersComponent } from '../../primeng/components/users/user.component';

const routes: Routes = [
    {
        path: 'users',
        component: UsersComponent
    },
    {
        path: '',
        component: BasicDataComponent
    },
    {
        path: 'roles',
        component: CNDListComponent
    },
    {
        path: 'permissions',
        component: CNDListComponent
    },
    {
        path: 'divisions',
        component: CNDListComponent
    },
    {
        path: 'zones',
        component: CNDListComponent
    },
    {
        path: 'areas',
        component: CNDListComponent
    },
    {
        path: 'blocks',
        component: CNDListComponent
    },
    {
        path: 'sub-blocks',
        component: CNDListComponent
    },
    {
        path: 'grades',
        component: CNDListComponent
    },
    {
        path: 'qualities',
        component: CNDListComponent
    },
    {
        path: 'basicdatatypes',
        component: CNDListComponent
    },
    {
        path: 'basicdatas',
        component: CNDListComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class BasicDataRoutingModule { }
