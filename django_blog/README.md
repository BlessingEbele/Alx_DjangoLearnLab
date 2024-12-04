<!-- 1. add steps to set up the project.
2. description of the authentication system and its componemts
3. instructions for testing authentication features.  -->

Explanation of the URL Patterns
/login/:

Maps to Django’s LoginView to handle user login.
Associated template: blog/login.html.
/logout/:

Maps to Django’s LogoutView to handle user logout.
Associated template: blog/logout.html.
/register/:

Maps to a custom register view for user registration.
Associated template: blog/register.html.
/profile/:

Maps to a custom profile view for viewing and editing user profile details.
Requires user authentication (@login_required decorator).
Associated template: blog/profile.html.