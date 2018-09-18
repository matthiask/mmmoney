from django.contrib import auth, messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from authlib.google import GoogleOAuth2Client


def oauth(request):
    client = GoogleOAuth2Client(request)

    if all(key not in request.GET for key in ("code", "oauth_token")):
        return redirect(client.get_authentication_url())

    user_data = client.get_user_data()

    if user_data.get("email"):
        user = auth.authenticate(email=user_data["email"])
        if user and user.is_active:
            auth.login(request, user)
            return redirect("/")

        messages.error(request, _("No user with email address or user inactive."))

    else:
        messages.error(request, _("Did not get an email address. Please try again."))

    return redirect("login")
