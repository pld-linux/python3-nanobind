# Conditional build:
%bcond_with	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	nanobind
Summary:	nanobind: tiny and efficient C++/Python bindings
Name:		python3-%{module}
Version:	2.7.0
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/n/nanobind/%{module}-%{version}.tar.gz
# Source0-md5:	c7d3eec4824b9f206781d68d12c326ec
URL:		https://pypi.org/project/nanobind/
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-installer
%if %{with tests}
#BuildRequires:	python3-
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nanobind is a small binding library that exposes C++ types in Python
and vice versa. It is reminiscent of Boost.Python and pybind11 and
uses near-identical syntax. In contrast to these existing tools,
nanobind is more efficient: bindings compile in a shorter amount of
time, produce smaller binaries, and have better runtime performance.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=typing_extensions \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
