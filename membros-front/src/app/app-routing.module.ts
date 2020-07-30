import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MembersDetailComponent } from './members-detail/members-detail.component';
import { NewMemberComponent } from './new-member/new-member.component';
import { NewEventComponent } from './new-event/new-event.component';
import { EventsDetailComponent } from './events-detail/events-detail.component';

/*
  aqui estão as rotas para acessar os demais componentes do aplicativo angular.
 */

 //constante de rotas onde colocaremos nossa estrutura de rotas
const routes: Routes = [
  { path: 'member-detail/:id', component: MembersDetailComponent},
  { path: 'new-member', component: NewMemberComponent},

  //paths de Event
  { path: 'event-detail/:id', component: EventsDetailComponent},
  { path: 'new-event', component: NewEventComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [ MembersDetailComponent, ]
