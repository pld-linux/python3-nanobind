#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	nanobind
Summary:	nanobind: tiny and efficient C++/Python bindings
Summary(pl.UTF-8):	nanobind - mały i wydajne wiązania C++/Python
Name:		python3-%{module}
Version:	2.15.0
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/n/nanobind/%{module}-%{version}.tar.gz
# Source0-md5:	638c0b45b652937963ea82264718427f
Patch0:		nanobind-eigen-32bit-index.patch
URL:		https://pypi.org/project/nanobind/
BuildRequires:	cmake >= 3.15
BuildRequires:	ninja
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-installer
BuildRequires:	python3-scikit-build-core >= 0.10
%if %{with tests}
BuildRequires:	eigen3 >= 3.3.1
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	python3-pytest
%ifarch %{ix86}
BuildRequires:	cpuinfo(sse2)
%endif
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-sphinx_copybutton >= 0.5.1
BuildRequires:	python3-sphinxcontrib-moderncmakedomain >= 3.29.0
BuildRequires:	python3-sphinxcontrib-svg2pdfconverter >= 1.2.2
BuildRequires:	sphinx-pdg-3 >= 6.1.3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nanobind is a small binding library that exposes C++ types in Python
and vice versa. It is reminiscent of Boost.Python and pybind11 and
uses near-identical syntax. In contrast to these existing tools,
nanobind is more efficient: bindings compile in a shorter amount of
time, produce smaller binaries, and have better runtime performance.

%description -l pl.UTF-8
nanobind to mała biblioteka wiążąca, udostępniająca typy C++ w
Pythonie i na odwrót. Przypomina Boost.Python i pybind11 i
wykorzystuje bardzo podobną składnię. W odróżnieniu od tamtych
bibliotek jest bardziej wydajna: wiązania kompilują się krócej,
tworzą mniejsze binaria i mają lepszą wydajność w czasie
wykonywania.

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
%patch -P0 -p1

%build
%py3_build_pyproject

%if %{with tests}
%cmake -B build-tests

%{__make} -C build-tests

cd build-tests
# test_chrono_steady_clock_roundtrip fails (as of 2.12.0)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -k 'not test_chrono_steady_clock_roundtrip'
cd ..
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,*.html,*.js}
%endif
