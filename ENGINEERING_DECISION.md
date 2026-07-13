1. PROJECT STRUCTURE 
    CC_PROJECT
        users : for authentications process(login,register,logout system)
        teams : Handling team functionality(adding users in team, creating team)


    organised it in this way so that each functionality stays in different app, which will keep code organised

    Django provides a lot of functionality handy, and django is my first framework which i learnt.Especially the generic views gives a lots of fucntionality, so that i don't have to write much code, also the common register,login,logout functionality is very easily done here


2. Database Design

    • Entity relationships
        Team model : Team.members has many-to-many relationship with TeamMembership model, which stores user's role with their respective team.

    • Why Table structure like this
        1. TeamMembership table stores user's team and their role in team, keeping data organized
        2.  

5. Problems faced
    1. Got same error many times about:
        Reverse for 'my_view_name' with keyword arguments '{'pk': ''}' not found. 1 pattern(s) tried: ['team/(?<pk>[0-9]+)/invitations/\\Z']

        Understood that it was due to pk values passed in url link in html file,
        In some cases it happened due to context was not passed in return render, so even if i used an pk id with some, it was unable to fetch id
        In some views like accept_invite_request i just copied and pasted(made some changes) the accept_join_request view, which had two id's passed, but later understood that there was no need of team.id as invite request visible to user was not specific to a team

    2. Showing error messages in generic class based view
        As generic CBV shows 403 forbidden when a user is not authorized, or has not permission to perform a task,
        searched about it online to change that error to a proper error message for CBV, 
        got a function called handle_no_permission which redirects and creates an error message, 
        also i could have created a custom UserAccessMixin, to create such error message

    3. No project found matching the query[got this error when i went to project update view url]
        when i tried to look at data retrieved i.e the team id and project id, they were correct.
        means the update view is not perceiving it correctly.
        the issue was that by default the generic view takes pk as id of the model used, but i used pk for my team id, 
        so later i changed url name for team id to team_pk and for project id pk

    4. Unable to redisplay older data for updateview
        update project button had post request and hence it was unable to retrieve data

    5. tasks.Task.assigned_to: (fields.E304) Reverse accessor 'User.task_set' for 'tasks.Task.assigned_to' clashes with        reverse accessor for 'tasks.Task.created_by'.
    HINT: Add or change a related_name argument to the definition for 'tasks.Task.assigned_to' or 'tasks.Task.created_by'.
    tasks.Task.created_by: (fields.E304) Reverse accessor 'User.task_set' for 'tasks.Task.created_by' clashes with reverse accessor for 'tasks.Task.assigned_to'
        Same reverse connection name was created for both created_by and assigned_to field, therefore i had to give them some differnt name using related name.

    6. When i was creating task with generic TaskCreateView, it was assigning task to every member in team.
    7. when_reject_join_request() funtion was passed, it gave error that : reject_join_request() got an unexpected keyword argument 'pk'
    searched more about it on google, the error was due to correct pk name was not passed, i mistakenly passed only pk for team id but it was actually team_pk
    


6. Tradeoff
    1. although owner is saved in teamMembership model , i stored owner in Team model itself, for easily retrieving owner of team, as it is frequently used.
    2. I didn't made Team field in task model as task model has project field which is using Project model , which already has the team field in it, so no need to save it in task. It was just making database redundant.


