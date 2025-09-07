import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LayoutComponent } from './layout.component';

const routes: Routes = [
    {
        path: '',
        component: LayoutComponent,
        children: [
            { path: '', redirectTo: 'dashboard', pathMatch: 'prefix' },
            {
                path: 'dashboard',
                loadChildren: () => import('./dashboard/dashboard.module').then((m) => m.DashboardModule)
            },
            {
                path: 'synthetic-data',
                loadChildren: () => import('./syntheticdata/syntheticdata.module').then((m) => m.SyntheticDataModule)
            },
            {
                path: 'dags',
                loadChildren: () => import('./dags/dags.module').then((m) => m.DagsModule)
            },
            {
                path: 'exams',
                loadChildren: () => import('./exams/exams.module').then((m) => m.ExamsModule)
            },
            {
                path: 'basic-data',
                loadChildren: () => import('./basicdata/basicdata.module').then((m) => m.BasicDataModule)
            },
            {
                path: 'harvesting',
                loadChildren: () => import('./harvesting/harvesting.module').then((m) => m.HarvestingModule)
            },
            {
                path: 'charts',
                loadChildren: () => import('./charts/charts.module').then((m) => m.ChartsModule)
            },
            {
                path: 'tables',
                loadChildren: () => import('./tables/tables.module').then((m) => m.TablesModule)
            },
            {
                path: 'forms',
                loadChildren: () => import('./form/form.module').then((m) => m.FormModule)
            },
            {
                path: 'bs-element',
                loadChildren: () => import('./bs-element/bs-element.module').then((m) => m.BsElementModule)
            },
            {
                path: 'grid',
                loadChildren: () => import('./grid/grid.module').then((m) => m.GridModule)
            },
            {
                path: 'components',
                loadChildren: () => import('./bs-component/bs-component.module').then((m) => m.BsComponentModule)
            },
            {
                path: 'blank-page',
                loadChildren: () => import('./blank-page/blank-page.module').then((m) => m.BlankPageModule)
            }
        ]
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class LayoutRoutingModule {}
