"""GraphQL views using Strawberry."""
from strawberry.django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from apps.graphql.schema import schema


class PublicGraphQLView(GraphQLView):
    """Public GraphQL endpoint with Strawberry."""
    pass


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    """Private GraphQL endpoint requiring authentication."""
    pass


@csrf_exempt
def graphql_playground(request):
    """GraphQL Playground view for development."""
    if request.method == 'GET':
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset=utf-8/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>GraphQL Playground</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
            <link rel="shortcut icon" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/favicon.png" />
            <script src="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
        </head>
        <body>
            <div id="root"></div>
            <script>
                window.addEventListener('load', function (event) {
                    GraphQLPlayground.init(document.getElementById('root'), {
                        endpoint: '/graphql/',
                        subscriptionEndpoint: 'ws://localhost:8000/graphql/',
                        settings: {
                            'request.credentials': 'include',
                            'editor.theme': 'dark',
                            'editor.fontSize': 14,
                            'editor.reuseHeaders': true,
                            'tracing.hideTracingResponse': false,
                            'editor.fontFamily': '"Fira Code", "Monaco", monospace',
                            'request.globalHeaders': {}
                        },
                        tabs: [
                            {
                                endpoint: '/graphql/',
                                query: `# Welcome to GraphQL Playground (Strawberry)
# 
# GraphQL Playground is an in-browser tool for writing, validating, and
# testing GraphQL queries.
#
# Type queries into this side of the screen, and you will see intelligent
# typeaheads aware of the current GraphQL type schema and live syntax and
# validation errors highlighted within the text.
#
# Keyboard shortcuts:
#  Prettify Query:  Shift-Ctrl-P (or press the prettify button above)
#     Run Query:  Ctrl-Enter (or press the play button above)
#   Auto Complete:  Ctrl-Space (or just start typing)

# Get current user
query GetMe {
  me {
    id
    email
    username
    firstName
    lastName
    isCompleteProfile
    fullName
  }
}

# Search users
query SearchUsers {
  users(search: "john", limit: 10) {
    id
    email
    username
    fullName
  }
}

# Login
mutation Login {
  login(input: {
    email: "admin@example.com"
    password: "admin123"
  }) {
    user {
      id
      email
      username
    }
    token
    refreshToken
  }
}

# Register new user
mutation Register {
  register(input: {
    email: "newuser@example.com"
    username: "newuser"
    password: "password123"
    firstName: "New"
    lastName: "User"
  }) {
    user {
      id
      email
    }
    token
    refreshToken
  }
}

# Update profile
mutation UpdateProfile {
  updateProfile(input: {
    firstName: "John"
    lastName: "Doe"
    bio: "Software Developer"
    phoneNumber: "+1234567890"
  }) {
    id
    email
    firstName
    lastName
    bio
    phoneNumber
    isCompleteProfile
  }
}

# Change password
mutation ChangePassword {
  changePassword(
    oldPassword: "currentpass"
    newPassword: "newpass123"
  ) {
    success
    message
  }
}

# Request password reset
mutation RequestPasswordReset {
  requestPasswordReset(email: "user@example.com") {
    success
    message
  }
}`
                            }
                        ]
                    })
                })
            </script>
        </body>
        </html>
        """
        return HttpResponse(html, content_type='text/html')
    return HttpResponse(status=405)


# Create view instances
public_graphql_view = csrf_exempt(PublicGraphQLView.as_view(schema=schema))
private_graphql_view = csrf_exempt(PrivateGraphQLView.as_view(schema=schema))