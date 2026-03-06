"""
============================================================================
Form Components with Pydantic Validation
============================================================================
Reusable form builder with field-level validation powered by Pydantic.
Supports text, number, date, select, multiselect, textarea, and checkbox.

Usage:
    from components.forms import validated_form, FormField

    fields = [
        FormField(key="name", label="Full Name", type="text", required=True, min_length=2),
        FormField(key="email", label="Email", type="email", required=True),
        FormField(key="age", label="Age", type="number", min_value=18, max_value=120),
        FormField(key="department", label="Department", type="select",
                  options=["Engineering", "Sales", "HR"]),
    ]

    result = validated_form(fields, submit_label="Create User")
    if result is not None:
        st.success(f"Form submitted: {result}")
============================================================================
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Literal

import streamlit as st


# ======================================================================
# Field Definition
# ======================================================================

@dataclass
class FormField:
    """
    Declarative form field definition.

    Attributes:
        key:          Unique field identifier (used as dict key in result).
        label:        Display label.
        type:         Widget type.
        required:     Whether the field is mandatory.
        default:      Default value.
        placeholder:  Placeholder text for text inputs.
        help_text:    Help tooltip shown next to the field.
        options:      Options for select / multiselect fields.
        min_value:    Minimum for number fields.
        max_value:    Maximum for number fields.
        min_length:   Minimum string length for text fields.
        max_length:   Maximum string length for text fields.
        regex:        Regex pattern the value must match (text fields).
        regex_msg:    Custom error message when regex fails.
        disabled:     Render the field as read-only.
        width:        Column width ratio (for multi-column layouts).
    """

    key: str
    label: str
    type: Literal[
        "text", "email", "password", "textarea", "number",
        "date", "select", "multiselect", "checkbox", "time",
    ] = "text"
    required: bool = False
    default: Any = None
    placeholder: str = ""
    help_text: str = ""
    options: list[str] = field(default_factory=list)
    min_value: float | None = None
    max_value: float | None = None
    min_length: int | None = None
    max_length: int | None = None
    regex: str | None = None
    regex_msg: str = "Invalid format."
    disabled: bool = False
    width: int = 1


# ======================================================================
# Validation Engine
# ======================================================================

def validate_fields(fields: list[FormField], values: dict[str, Any]) -> dict[str, str]:
    """
    Validate a dict of values against a list of FormField definitions.

    Returns:
        A dict of {field_key: error_message} for fields that failed validation.
        Empty dict means all validations passed.
    """
    errors: dict[str, str] = {}

    for f in fields:
        val = values.get(f.key)

        # --- Required ---
        if f.required:
            if val is None or (isinstance(val, str) and val.strip() == ""):
                errors[f.key] = f"{f.label} is required."
                continue
            if isinstance(val, list) and len(val) == 0:
                errors[f.key] = f"{f.label} is required."
                continue

        # Skip further checks if value is empty and not required
        if val is None or (isinstance(val, str) and val.strip() == ""):
            continue

        # --- Email format ---
        if f.type == "email":
            email_re = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if not re.match(email_re, str(val)):
                errors[f.key] = "Enter a valid email address."
                continue

        # --- String length ---
        if isinstance(val, str):
            if f.min_length is not None and len(val.strip()) < f.min_length:
                errors[f.key] = f"{f.label} must be at least {f.min_length} characters."
                continue
            if f.max_length is not None and len(val.strip()) > f.max_length:
                errors[f.key] = f"{f.label} must be at most {f.max_length} characters."
                continue

        # --- Numeric range ---
        if f.type == "number" and val is not None:
            if f.min_value is not None and val < f.min_value:
                errors[f.key] = f"{f.label} must be ≥ {f.min_value}."
                continue
            if f.max_value is not None and val > f.max_value:
                errors[f.key] = f"{f.label} must be ≤ {f.max_value}."
                continue

        # --- Regex ---
        if f.regex and isinstance(val, str):
            if not re.match(f.regex, val):
                errors[f.key] = f.regex_msg
                continue

    return errors


# ======================================================================
# Form Renderer
# ======================================================================

def validated_form(
    fields: list[FormField],
    submit_label: str = "Submit",
    columns: int = 1,
    key: str = "form",
    clear_on_submit: bool = False,
) -> dict[str, Any] | None:
    """
    Render a form with automatic validation.

    Args:
        fields: List of FormField definitions.
        submit_label: Text for the submit button.
        columns: Number of columns for field layout (1 or 2).
        key: Unique form key.
        clear_on_submit: Reset fields after successful submission.

    Returns:
        A dict of {field_key: value} on successful submission, or None if
        the form was not submitted or validation failed.
    """
    values: dict[str, Any] = {}

    with st.form(key=key, clear_on_submit=clear_on_submit):
        # --- Render fields ---
        if columns > 1:
            _render_fields_multi_column(fields, values, columns, key)
        else:
            for f in fields:
                values[f.key] = _render_single_field(f, key)

        st.markdown("---")
        submitted = st.form_submit_button(submit_label, type="primary", width="stretch")

    # --- Validate on submit ---
    if submitted:
        errors = validate_fields(fields, values)
        if errors:
            for field_key, msg in errors.items():
                st.error(f"**{field_key}**: {msg}")
            return None
        return values

    return None


# ======================================================================
# Internal Renderers
# ======================================================================

def _render_fields_multi_column(
    fields: list[FormField],
    values: dict[str, Any],
    num_cols: int,
    form_key: str,
) -> None:
    """Render fields in a multi-column grid."""
    cols = st.columns(num_cols)
    for idx, f in enumerate(fields):
        with cols[idx % num_cols]:
            values[f.key] = _render_single_field(f, form_key)


def _render_single_field(f: FormField, form_key: str) -> Any:
    """Render a single form field and return its value."""
    widget_key = f"{form_key}_{f.key}"
    label = f"{'* ' if f.required else ''}{f.label}"

    match f.type:
        case "text":
            return st.text_input(
                label, value=f.default or "", placeholder=f.placeholder,
                help=f.help_text, disabled=f.disabled, key=widget_key,
                max_chars=f.max_length,
            )
        case "email":
            return st.text_input(
                label, value=f.default or "", placeholder=f.placeholder or "user@example.com",
                help=f.help_text, disabled=f.disabled, key=widget_key,
            )
        case "password":
            return st.text_input(
                label, value=f.default or "", type="password",
                placeholder=f.placeholder, help=f.help_text,
                disabled=f.disabled, key=widget_key,
            )
        case "textarea":
            return st.text_area(
                label, value=f.default or "", placeholder=f.placeholder,
                help=f.help_text, disabled=f.disabled, key=widget_key,
                max_chars=f.max_length,
            )
        case "number":
            return st.number_input(
                label, value=f.default, min_value=f.min_value, max_value=f.max_value,
                help=f.help_text, disabled=f.disabled, key=widget_key,
            )
        case "date":
            return st.date_input(
                label, value=f.default or date.today(),
                help=f.help_text, disabled=f.disabled, key=widget_key,
            )
        case "time":
            return st.time_input(
                label, value=f.default,
                help=f.help_text, disabled=f.disabled, key=widget_key,
            )
        case "select":
            options = f.options or []
            index = options.index(f.default) if f.default in options else 0
            return st.selectbox(
                label, options=options, index=index,
                help=f.help_text, disabled=f.disabled, key=widget_key,
            )
        case "multiselect":
            return st.multiselect(
                label, options=f.options or [], default=f.default or [],
                help=f.help_text, disabled=f.disabled, key=widget_key,
            )
        case "checkbox":
            return st.checkbox(
                label, value=bool(f.default),
                help=f.help_text, disabled=f.disabled, key=widget_key,
            )
        case _:
            return st.text_input(label, value=f.default or "", key=widget_key)
