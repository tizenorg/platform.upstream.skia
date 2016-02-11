. $(dirname $0)/common.sh

function silentApply() {
  PATCH=$(readlink -f $1)
  patch -d ${TOPDIR} --forward --reject-file=- -p1 -i $PATCH >/dev/null
  if [ "$?" -gt 0 ]; then
    >&2 echo "failed applying $1"
  fi
}

function silentDeapply() {
  PATCH=$(readlink -f $1)
  pushd ${TOPDIR} > /dev/null
  patch --forward --reject-file=- -p1 --dry-run -i $PATCH >/dev/null
  RET=$?
  if [ "$RET" -gt 1 ]; then
    >&2 echo "failed deapplying $1"
  elif [ "$RET" == "1" ]; then
    # exit status 1 means it's already applied so we revert
    patch -p1 -R --reject-file=- -i $PATCH >/dev/null
  fi
  popd > /dev/null
}

echo "$@" | grep -q "\-r" && REVERSE=1

patchdir=${TOPDIR}/build/patches

if [ -f $patchdir/*.diff ]; then
  for patch in $patchdir/*.diff; do
    if [ -z "$REVERSE" ]; then
      silentApply $patch
    else
      silentDeapply $patch
    fi
  done
fi
