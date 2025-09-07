import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DagsComponent } from './components/dags/dags.component';
import { KcsComponent } from './components/kcs/kcs.component';
import { QuestionsComponent } from './components/questions/questions.component';
import { DagedgesComponent } from './components/dagedges/dagedges.component';
import { OptionsComponent } from './components/questions/options.component';

const routes: Routes = [
    {
        path: 'kcs',
        component: KcsComponent
    },
    {
        path: 'dags',
        component: DagsComponent
    },
    {
        path: 'dagedges',
        component: DagedgesComponent
    },
    {
        path: 'questions',
        component: QuestionsComponent
    },
    {
        path: 'options',
        component: OptionsComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class DagsRoutingModule { }
