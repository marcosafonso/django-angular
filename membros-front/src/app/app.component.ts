import { Component } from '@angular/core';
import { ApiService} from './api.service';
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

  constructor(private api:ApiService) {
    this.getMembers();
  }
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
    this.api.getMember(member.id).subscribe(
      data => {
        console.log(data);
      },
      error => {
        console.log("Aconteceu um erro", error.message);
      }
    )
  };

}


