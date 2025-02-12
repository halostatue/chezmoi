# `gitHubLatestTag` *owner-repo*

`gitHubLatestTag` calls the GitHub API to retrieve the latest tag for the given
*owner-repo*, returning structured data as defined by the [GitHub Go API
bindings][bindings].

Calls to `gitHubLatestTag` are cached the same as [`githubTags`][tags],
so calling `gitHubLatestTag` with the same *owner-repo* will only result in one
call to the GitHub API.

!!! example

    ```
    {{ (gitHubLatestTag "docker/compose").Name }}
    ```

!!! warning

    The `gitHubLatestTag` returns the first tag returned by the [list repository
    tags GitHub API endpoint][endpoint]. Although this seems to be the most
    recent tag, the GitHub API documentation does not specify the order of the
    returned tags.

[bindings]: https://pkg.go.dev/github.com/google/go-github/v68/github#RepositoryTag
[tags]: site:reference/templates/github-functions/gitHubTags/
[endpoint]: https://docs.github.com/en/rest/repos/repos#list-repository-tags
