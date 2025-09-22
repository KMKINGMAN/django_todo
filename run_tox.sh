#!/bin/bash
# Tox helper script for Django Todo project

set -e

echo "🧪 Django Todo Project - Tox Test Runner"
echo "========================================"

function show_help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Available commands:"
    echo "  test          - Run tests on all Python versions"
    echo "  lint          - Run linting (flake8, black, isort)"
    echo "  format        - Format code with black and isort"
    echo "  type-check    - Run mypy type checking"
    echo "  security      - Run security checks (bandit, safety)"
    echo "  coverage      - Run tests with coverage report"
    echo "  django-check  - Run Django system checks"
    echo "  integration   - Run only integration tests"
    echo "  api-tests     - Run only API tests"
    echo "  unit-tests    - Run only unit tests"
    echo "  fast          - Run tests quickly (fail fast)"
    echo "  clean         - Clean tox environments"
    echo "  recreate      - Recreate all tox environments"
    echo "  help          - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 test                    # Run all tests"
    echo "  $0 lint                    # Check code style"
    echo "  $0 coverage                # Run with coverage"
    echo "  $0 fast -- -k test_todo    # Run specific test quickly"
}

case ${1:-help} in
    test)
        echo "🔬 Running tests on all Python versions..."
        tox -e py310,py311,py312 "${@:2}"
        ;;
    lint)
        echo "🧹 Running linting checks..."
        tox -e pylint "${@:2}"
        ;;
    format)
        echo "✨ Formatting code..."
        tox -e format "${@:2}"
        ;;
    type-check)
        echo "🔍 Running type checking..."
        tox -e type-check "${@:2}"
        ;;
    security)
        echo "🔒 Running security checks..."
        tox -e security "${@:2}"
        ;;
    coverage)
        echo "📊 Running tests with coverage..."
        tox -e coverage "${@:2}"
        ;;
    django-check)
        echo "⚙️  Running Django system checks..."
        tox -e django-check "${@:2}"
        ;;
    integration)
        echo "🔗 Running integration tests..."
        tox -e integration "${@:2}"
        ;;
    api-tests)
        echo "🌐 Running API tests..."
        tox -e api-tests "${@:2}"
        ;;
    unit-tests)
        echo "🧪 Running unit tests..."
        tox -e unit-tests "${@:2}"
        ;;
    fast)
        echo "⚡ Running tests quickly..."
        tox -e fast "${@:2}"
        ;;
    clean)
        echo "🧽 Cleaning tox environments..."
        tox --clean
        ;;
    recreate)
        echo "🔄 Recreating all environments..."
        tox -r
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

echo "✅ Done!"
