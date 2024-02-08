#!/usr/bin/env bash

case "$OSTYPE" in
    msys*)    python=python ;;
    cygwin*)  python=python ;;
    *)        python=python3 ;;
esac
ls -a
cd ../yacut/
echo "from yacut import db; \
     from yacut.models import URLMap; \
     db.create_all(); \
     URLMap.query.delete(); \
     url_map_object = URLMap(original='https://example.com/', short='example'); db.session.add(url_map_object); db.session.commit()" | flask shell >/dev/null 2>&1
cd -
