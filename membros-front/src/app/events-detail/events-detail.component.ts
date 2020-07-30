import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, ParamMap } from '@angular/router';
import { ApiService} from './api.service';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-events-detail',
  templateUrl: './events-detail.component.html',
  styleUrls: ['./events-detail.component.css']
})
export class EventsDetailComponent implements OnInit {

  constructor(    
    // ActivatedRoute nos dá acesso a rota ativa no momento, seus parâmetros e demais valores
    private route: ActivatedRoute, 
    private api:ApiService,
    private router: Router,
    private appComponent: AppComponent) { }

    selected_event = {id: '', name: '', describe: ''};
    selected_id ;

  ngOnInit() {
    this.route.paramMap.subscribe((param: ParamMap) => {
      let id = parseInt(param.get('id'));
      this.selected_id = id;
      this.loadEvent(id);
    });
  }

  loadEvent(id){
    this.api.getEvent(id).subscribe(
      data => {
        console.log(data);
        this.selected_event = data;
      },
      error => {
        console.log("Aconteceu um erro", error.message);
      }
    )
  };

  update(){
    this.api.updateEvent(this.selected_event).subscribe(
      data => {
        this.selected_event = data;
      },
      error => {
        console.log("Aconteceu um erro", error.message);
      }
    )
  };

  delete(){
    this.api.deleteEvent(this.selected_id).subscribe(
      data => {
        let index;
        this.appComponent.events.forEach((e, i) =>{
          if(e.id == this.selected_id)
            index = i;
        });
        this.appComponent.events.splice(index, 1);
      },
      error => {
        console.log("Aconteceu um erro", error.message);
      }
    )
  };

  newEvent(){
    this.router.navigate(['new-event']);
  }

}
