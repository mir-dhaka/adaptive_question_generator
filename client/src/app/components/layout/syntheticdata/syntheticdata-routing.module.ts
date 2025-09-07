import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router'; 
import { CNDListComponent } from '../../primeng/components/list/cndlist';
import { UsersComponent } from '../../primeng/components/users/user.component';
import { StudentRawDataComponent } from './components/rawdata/studentrawdata.component';
import { ExamRawDataComponent } from './components/rawdata/examrawdata.component';
import { CalculatedMasteryComponent } from './components/calculated-mastery/calculatedmastery.component';

const routes: Routes = [
    {
        path: 'student-data',
        component: StudentRawDataComponent
    },
    {
        path: 'exam-data',
        component: ExamRawDataComponent
    },
    {
        path: 'calculated-mastery',
        component: CalculatedMasteryComponent
    },
    {
        path: 'featuredev',
        component: CNDListComponent
    },
    {
        path: 'student-profile',
        component: CNDListComponent
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class SyntheticDataRoutingModule { }
