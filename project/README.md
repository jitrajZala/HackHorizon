# College Hackathon Platform

A Django-based web application for managing and participating in college hackathons.

## Features

- **Hackathon Management**: Create, view, and manage hackathons
- **Team Formation**: Create teams and invite members
- **Project Submission**: Submit projects with GitHub links, demos, and presentations
- **Results & Judging**: View hackathon results and rankings
- **User Dashboard**: Track participation and submissions

## Setup Instructions

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py migrate
   ```

3. Create a superuser (for admin access):
   ```
   python manage.py createsuperuser
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

5. Access the application at http://127.0.0.1:8000/

## Admin Access

The Django admin interface is available at http://127.0.0.1:8000/admin/

Use the superuser credentials created in step 3 to log in and manage:
- Hackathons
- Teams
- Participants
- Submissions
- Announcements

## Project Structure

- `hackathon_project/`: Main project settings
- `hackathons/`: Main application
  - `models.py`: Database models
  - `views.py`: View functions and classes
  - `forms.py`: Form definitions
  - `urls.py`: URL routing
  - `admin.py`: Admin interface configuration
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript, images)
- `media/`: User-uploaded files

## Usage

### For Students

1. Register an account
2. Browse available hackathons
3. Create or join a team
4. Submit your project
5. View results after the hackathon ends

### For Administrators

1. Log in to the admin interface
2. Create and manage hackathons
3. Review team registrations
4. Score submissions
5. Publish results

## License

This project is licensed under the MIT License - see the LICENSE file for details.