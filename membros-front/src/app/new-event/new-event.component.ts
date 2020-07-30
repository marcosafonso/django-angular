import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-new-event',
  templateUrl: './new-event.component.html',
  styleUrls: ['./new-event.component.css']
})
export class NewEventComponent implements OnInit {

  event = {name: '', describe: ''};

  constructor(
    private api: ApiService,
    private appComponent: AppComponent) { }

  ngOnInit(): void {
  }

  save(){
    this.api.saveNewEvent(this.event).subscribe(
      data => {
        this.appComponent.events.push(data);
      },
      error => {
        console.log("Aconteceu um erro", error.message);
      }
    )
  }

}
