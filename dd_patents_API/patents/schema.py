from rest_framework import serializers

class IncludeParam(serializers.Serializer):
    include = serializers.CharField(
        required=False,
        help_text=(
            "Comma‑separated list of relations to embed "
            "(abstracts, claims, disclosures, interested_parties, "
            "priority_claims, ipc_classifications, or 'all')."
        ),
    )
    fields = serializers.CharField(
        required=False,
        help_text="Comma‑separated list of fields to return (supports dotted paths).",
    )
