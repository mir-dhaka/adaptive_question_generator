import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CNDListComponent } from '../../primeng/components/list/cndlist'; 
import { NewExamComponent } from './components/newexam.component';
import { ExamDetailsComponent } from './components/examexamdetails.component';

const routes: Routes = [
    {
        path: 'start',
        component: NewExamComponent
    },
    {
        path: 'details',
        component: ExamDetailsComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ExamsRoutingModule { }
