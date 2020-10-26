import { Component } from '@angular/core';
import { ApiService} from './api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'membros-front';

  members = [
    {name: 'Fulano', id: 1, surname: "Cicrano", photo: 'http://localhost:8000/members/members_profile/mario.jpg'},
    {name: 'Beltrano', id: 1, surname: "Cicrano", photo: 'http://localhost:8000/members/members_profile/mario.jpg'},
  ];

  events = [
    {id: '', name: '', describe: ''}
  ]

  fulanos = [
    {id: '', nome: '', ativo: '', data_modificacao: ''}
  ]

  constructor(private api:ApiService, private router: Router) {
    this.getMembers();
    this.getEvents();
    this.getFulanos();
  }

  getFulanos = () => {
    this.api.getAllFulanos().subscribe(
      data => {
        this.fulanos = data
      },
      error => {
        console.log("Aconteceu um erro oh not.");
      }
    );
  };

  getMembers = () => {
    this.api.getAllMembers().subscribe(
      data => {
        this.members = data
      },
      error => {
        console.log("Aconteceu um erro.");
      }
    );
  };

  memberClicked = (member) => {
    this.router.navigate(['member-detail', member.id]);
  };

// funcoes para Event

  eventClicked = (event) => {
    this.router.navigate(['event-detail', event.id]);
  };

  getEvents = () => {
    this.api.getAllEvents().subscribe(
      data => {
        this.events = data
      },
      error => {
        console.log("Aconteceu um erro.");
      }
    );
  };

}


