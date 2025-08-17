"""GraphQL views."""
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    """GraphQL view that requires authentication."""
    pass


class PublicGraphQLView(GraphQLView):
    """Public GraphQL view."""
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
                                query: `# Welcome to GraphQL Playground
# 
# GraphQL Playground is an in-browser tool for writing, validating, and
# testing GraphQL queries.
#
# Type queries into this side of the screen, and you will see intelligent
# typeaheads aware of the current GraphQL type schema and live syntax and
# validation errors highlighted within the text.
#
# GraphQL queries typically start with a "{" character. Lines that start
# with a # are ignored.
#
# An example GraphQL query might look like:
#
#     {
#       me {
#         id
#         email
#         username
#       }
#     }
#
# Keyboard shortcuts:
#
#  Prettify Query:  Shift-Ctrl-P (or press the prettify button above)
#     Run Query:  Ctrl-Enter (or press the play button above)
#   Auto Complete:  Ctrl-Space (or just start typing)
#

query GetMe {
  me {
    id
    email
    username
    firstName
    lastName
  }
}

query GetAllUsers {
  allUsers(first: 10) {
    edges {
      node {
        id
        email
        username
      }
    }
  }
}

mutation Login {
  tokenAuth(email: "admin@example.com", password: "admin123") {
    token
    refreshToken
    user {
      id
      email
    }
  }
}

mutation Register {
  register(
    email: "newuser@example.com"
    username: "newuser"
    password: "password123"
    firstName: "New"
    lastName: "User"
  ) {
    success
    errors
    user {
      id
      email
    }
    token
  }
}

subscription OnlineUsers {
  onlineUsers {
    onlineUsers {
      id
      username
    }
    userJoined {
      id
      username
    }
    userLeft {
      id
      username
    }
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