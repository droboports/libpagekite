#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.68])

# libpagekite is Copyright 2011-2016, The Beanstalks Project ehf.

AC_INIT([libpagekite], [0.90.150224], [info@pagekite.net])
AM_INIT_AUTOMAKE([-Wall -Werror foreign])
AC_CONFIG_SRCDIR([libpagekite/pkconn.h])
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])
AC_CANONICAL_HOST


use_openssl="yes"
use_libev="yes"

specialssldir=""
AC_ARG_WITH(openssl,[  --with-openssl=DIR    Use optional openssl libs and includes from [DIR]/lib/ and [DIR]/include/openssl/],
[  case "$with_openssl" in
  yes)
  ;;
  no)
    use_openssl="no"
  ;;
  *)
    specialssldir="$with_openssl"
    LDFLAGS="$LDFLAGS -L$with_openssl/lib"
    CPPFLAGS="-I$with_openssl/include $CPPFLAGS"
  ;;
  esac]
)

AC_ARG_WITH(lua,
	[AS_HELP_STRING([--without-lua],
		[Do not compile pagekite lua bindings even if Lua is available])],
		[], [with_lua=yes])

AC_ARG_WITH(os-libev,
	[AS_HELP_STRING([--without-os-libev],
		[Use embedded libev, not the OS-provided library])],
		[use_libev=no], [])


AC_ARG_WITH(java,
	[AS_HELP_STRING([--without-java],
		[Do not compile pagekite java bindings even if Java is available])],
		[], [with_java=yes])

AC_ARG_WITH(agpl-relay,
	[AS_HELP_STRING([--with-agpl-relay],
		[Compile libpagekite relay support (AGPLv3 code)])],
		[with_relay=yes], [with_relay=no])

AC_ARG_WITH(ds-logfmt,
	[AS_HELP_STRING([--with-ds-logfmt],
		[Compile libpagekite with DigitalSTROM log format.])],
		[with_ds_logfmt=yes], [with_ds_logfmt=no])


# Checks for programs.
AC_PROG_CC
m4_ifdef([AM_PROG_AR], [AM_PROG_AR])
AC_LIBTOOL_WIN32_DLL
AC_PROG_LIBTOOL
#AC_PROG_INSTALL
AM_PROG_CC_C_O

LT_INIT

# Check for JNI, Java
if test "$with_java" = "yes"; then
	if test "x$JAVAC" = x; then
		JAVAC=javac
	fi
	AC_CHECK_PROG(_CHECK_JAVAC, [$JAVAC], yes)
	if test x"$_CHECK_JAVAC" != xyes; then
		AC_MSG_ERROR([cannot find javac; try setting \$JAVAC])
	fi

	# AX_JNI_INCLUDE_DIR fails when cross-compiling.
	# Skip it if jni.h can already be found in the default include path
	AC_CHECK_HEADER([jni.h],[],[
		AX_JNI_INCLUDE_DIR
		for JNI_INCLUDE_DIR in $JNI_INCLUDE_DIRS; do
		  CPPFLAGS="$CPPFLAGS -I$JNI_INCLUDE_DIR"
		done
        AC_SUBST(CPPFLAGS)
	])
    AS_UNSET([ac_cv_header_jni_h])
    AC_SUBST(JAVAC)
fi
AM_CONDITIONAL(HAVE_JAVA, test "x$with_java" = "xyes")

# Checks for header files.
AC_CHECK_HEADERS([jni.h pthread.h arpa/inet.h fcntl.h float.h inttypes.h limits.h netdb.h netinet/in.h stddef.h stdint.h stdlib.h string.h strings.h sys/socket.h sys/statfs.h sys/time.h sys/timeb.h unistd.h])

# Checks for libraries.
# FIXME: Replace `main' with a function in `-lpthread':
AC_CHECK_LIB([pthread], [main])

# Checks for typedefs, structures, and compiler characteristics.
m4_ifdef([AC_CHECK_HEADER_STDBOOL], [AC_CHECK_HEADER_STDBOOL])
AC_C_INLINE
AC_TYPE_INT16_T
AC_TYPE_INT32_T
AC_TYPE_INT64_T
AC_TYPE_INT8_T
AC_TYPE_PID_T
AC_TYPE_SIZE_T
AC_TYPE_SSIZE_T
AC_CHECK_MEMBERS([struct stat.st_rdev])
AC_TYPE_UINT16_T
AC_TYPE_UINT32_T
AC_TYPE_UINT64_T
AC_TYPE_UINT8_T

# Checks for library functions.
AC_FUNC_LSTAT_FOLLOWS_SLASHED_SYMLINK
AC_FUNC_MALLOC
AC_FUNC_REALLOC
AC_CHECK_FUNCS([clock_gettime dup2 gethostbyname gettimeofday inet_ntoa memmove memset select socket strcasecmp strchr strdup strerror strncasecmp strrchr uname pthread_yield pthread_yield_np])

# OpenSSL requires dlopen on some platforms
AC_SEARCH_LIBS(dlopen, dl)

# If they didn't specify it, we try to find it
if test "$use_openssl" = "yes" -a -z "$specialssldir" ; then
	AC_CHECK_HEADER(openssl/ssl.h,,
			[ use_openssl="no"
        AC_MSG_WARN([Failed to find openssl/ssl.h so OpenSSL will not be used. 
	If it is installed you can try the --with-openssl=DIR argument]) ])

	if test "$use_openssl" = "yes"; then
	     AC_CHECK_HEADER(openssl/err.h,,
	         [ use_openssl="no"
		     AC_MSG_WARN([Failed to find openssl/err.h so OpenSSL will not be used.
		      If it is installed you can try the --with-openssl=DIR argument]) ])
	fi

	if test "$use_openssl" = "yes"; then
		   AC_CHECK_HEADER(openssl/rand.h,,
		       [ use_openssl="no"
		         AC_MSG_WARN([Failed to find openssl/rand.h so OpenSSL will not be used.
			  If it is installed you can try the --with-openssl=DIR argument]) ])
	fi

	if test "$use_openssl" = "yes"; then
	 AC_CHECK_LIB(crypto, BIO_int_ctrl,
	   [],
	   [ use_openssl="no"
	   AC_MSG_WARN([Failed to find libcrypto so OpenSSL will not be used.
	    If it is installed you can try the --with-openssl=DIR argument]) ])
	fi
										     
	if test "$use_openssl" = "yes"; then
	   AC_CHECK_LIB(ssl, SSL_new,
	   [],
	   [ use_openssl="no"
	   AC_MSG_WARN([Failed to find libssl so OpenSSL will not be used. 
If it is installed you can try the --with-openssl=DIR argument]) ])
	fi
fi

OPENSSL_CFLAGS=""
OPENSSL_LIBS=""
if test "$use_openssl" = "yes"; then
  AC_DEFINE([HAVE_OPENSSL], [1], [Define to 1 if you have OpenSSL.])
  OPENSSL_LIBS="-lssl -lcrypto"
  # Define in Makefile also.
  HAVE_OPENSSL=yes
  AC_SUBST(HAVE_OPENSSL)
fi
AC_SUBST([OPENSSL_CFLAGS])
AC_SUBST([OPENSSL_LIBS])



LIBEV_CFLAGS=""
LIBEV_LIBS=""
if test "x${use_libev}" != "xno"; then
  AC_MSG_CHECKING([Enabled libev.])
  # libev
  AC_MSG_CHECKING([for libev support])
  AC_ARG_WITH([libev],
    [AS_HELP_STRING([--with-libev@<:@=PATH@:>@],[Search for libev in PATH/include and PATH/lib])],
    [WITH_LIBEV=$withval],[WITH_LIBEV=yes])
  PKG_CHECK_MODULES([LIBEV], [libev], [], [
    # no pkg-config for libev, searching manually:
    if test "$WITH_LIBEV" != "yes"; then
      LIBEV_CFLAGS="-I$WITH_LIBEV/include"
      LIBEV_LIBS="-L$WITH_LIBEV/lib -lev"
    else
      AC_CHECK_HEADERS([ev.h],[
        AC_CHECK_LIB([ev], [ev_time], [
          LIBEV_LIBS="-lev"
          ],[
          AC_MSG_ERROR([libev not found])
          ]
        )],[
          AC_MSG_ERROR([libev not found])
        ]
        )
    fi
  ])
fi
AC_SUBST([LIBEV_CFLAGS])
AC_SUBST([LIBEV_LIBS])


# Lua support

AS_IF([test "x$with_lua" != 'xno'],
	[ AX_PROG_LUA([5.1], [], [lua_interp='yes'], [lua_interp='no'])

    AS_IF([test "x$lua_interp" = 'xyes'],
      [ AX_LUA_HEADERS([lua_headers='yes'], [lua_headers='no'])
        AX_LUA_LIBS([lua_libs='yes'], [lua_libs='no'])
      ])

    AS_IF([test "x$lua_interp" = 'xyes' &&
           test "x$lua_headers" = 'xyes' &&
           test "x$lua_libs" = 'xyes'],
      [with_lua='yes'],
      [with_lua='no'])
  ])
AM_CONDITIONAL(HAVE_LUA, test "x$with_lua" = "xyes")
AC_SUBST([LUA_INCLUDE])
AC_SUBST([LUA_LIBS])

AS_IF([test "x$with_agpl_relay" = 'xyes'],
	[with_relay='yes'], [with_relay='no'])
AM_CONDITIONAL(HAVE_RELAY, test "x$with_relay" = "xyes")
if test "$with_relay" = "yes"; then
  AC_DEFINE([HAVE_RELAY], [1], [Define to 1 if you want AGPLv3 relay code.])
  HAVE_RELAY=1
fi


AS_IF([test "x$with_ds_logfmt" = 'xyes'],
	[with_ds_logfmt='yes'], [with_ds_logfmt='no'])
AM_CONDITIONAL(HAVE_DS_LOG_FORMAT, test "x$with_ds_logfmt" = "xyes")
if test "$with_ds_logfmt" = "yes"; then
  AC_DEFINE([HAVE_DS_LOG_FORMAT], [1], [Define to 1 to use DigitalSTROM log format.])
  HAVE_DS_LOGFMT=1
fi

JAVAROOT="\$(top_builddir)/java-classes/"
AC_SUBST(JAVAROOT)

AC_CONFIG_FILES([Makefile
  libpagekite/Makefile
  libpagekite/libpagekite.pc
  contrib/backends/Makefile
  contrib/relays/Makefile
  bindings/java/Makefile
])
AC_OUTPUT
