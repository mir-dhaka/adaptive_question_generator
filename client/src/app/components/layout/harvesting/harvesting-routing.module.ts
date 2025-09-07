import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CNDListComponent } from '../../primeng/components/list/cndlist';
import { FCPComponent } from '../../primeng/components/FCP/fruitcollectionpoint';
import { PlantationComponent } from '../../primeng/components/plantations/plantations';
import { TreesComponent } from '../../primeng/components/trees/trees';

const routes: Routes = [
    {
        path: '',
        component: CNDListComponent
    },
    {
        path: 'fruits-collection-points',
        component: FCPComponent
    },
    {
        path: 'plantations',
        component: PlantationComponent
    },
    {
        path: 'trees',
        component: TreesComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class HarvestingRoutingModule { }
