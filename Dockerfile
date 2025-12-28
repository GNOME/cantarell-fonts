FROM registry.fedoraproject.org/fedora:latest
RUN dnf install -y git-core libappstream-glib-devel gettext uv

ADD pyproject.toml uv.lock /src
WORKDIR /src
RUN uv sync

ADD appstream /src/appstream
ADD prebuilt /src/prebuilt
ADD scripts /src/scripts
ADD src /src/src
ADD meson.build meson_options.txt noxfile.py /src

RUN uv run nox -s build_variable
RUN git init
RUN uv run nox -s dist
#RUN uv cache prune --ci
