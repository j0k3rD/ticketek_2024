from unittest.mock import patch

from src.admin.admin_services import approve_registration

def test_approve_registration(setup_events, registration_data):
    session, event1, _ = setup_events

    registration_data.event_id = event1.id
    session.add(registration_data)
    session.commit()
    session.refresh(registration_data)

    # Usa unittest.mock.patch para mockear send_email
    with patch("src.admin.admin_services.send_email") as mock_send_email:
        approve_registration(session, registration_data.id)

        mock_send_email.assert_called_once()

        mock_send_email.assert_called_with(
            registration_data.email,
            "Registro Aprobado!",
            f"Su registro al evento {event1.title} ha sido aprobado. En caso de que quiera darse de baja deberá usar este token {registration_data.token}."
        )

        # Verifica que el estado de la inscripción es 'approved'
        assert registration_data.status == "approved"

        # Verifica que el token se ha generado
        assert registration_data.token is not None

        # Verifica que el asistente ha sido añadido al evento
        assert str(registration_data.id) in event1.attendees
        assert event1.attendees[str(registration_data.id)]["email"] == registration_data.email
