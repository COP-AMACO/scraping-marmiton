import unittest

from marmiton.simplify_string import simplify_string


class TestSimplifyString(unittest.TestCase):
    """Tests for the simplify_string function."""

    def test_accents_removal(self):
        """Test accent removal."""
        # Accented vowels
        self.assertEqual(simplify_string("café"), "cafe")
        self.assertEqual(simplify_string("crème"), "creme")
        self.assertEqual(simplify_string("pâte"), "pate")
        self.assertEqual(simplify_string("côte"), "cote")
        self.assertEqual(simplify_string("sûr"), "sur")

        # Accented consonants
        self.assertEqual(simplify_string("façon"), "facon")
        self.assertEqual(simplify_string("garçon"), "garcon")

        # Multiple accents
        self.assertEqual(simplify_string("pâtés"), "pates")
        self.assertEqual(simplify_string("crêpés"), "crepes")
        self.assertEqual(simplify_string("garçoñ"), "garcon")

    def test_ligatures_replacement(self):
        """Test ligature replacement."""
        self.assertEqual(simplify_string("œuf"), "oeuf")
        self.assertEqual(simplify_string("bœuf"), "boeuf")
        self.assertEqual(simplify_string("cœur"), "coeur")
        self.assertEqual(simplify_string("vitæ"), "vitae")

    def test_spaces_replacement(self):
        """Test space replacement with dashes."""
        self.assertEqual(simplify_string("tomate cerise"), "tomate-cerise")
        self.assertEqual(simplify_string("crème fraîche"), "creme-fraiche")
        self.assertEqual(simplify_string("pomme de terre"), "pomme-de-terre")

    def test_apostrophes_replacement(self):
        """Test apostrophe replacement with dashes."""
        self.assertEqual(simplify_string("l'œuf"), "l-oeuf")
        self.assertEqual(simplify_string("qu'est-ce"), "qu-est-ce")

    def test_lowercase_conversion(self):
        """Test conversion to lowercase."""
        self.assertEqual(simplify_string("CAFÉ"), "cafe")
        self.assertEqual(simplify_string("Crème"), "creme")
        self.assertEqual(simplify_string("TOMATE CERISE"), "tomate-cerise")
        self.assertEqual(simplify_string("L'ŒUF"), "l-oeuf")

    def test_combined_transformations(self):
        """Test combined transformations."""
        # Example from the code: "Café crème à l'œuf"
        self.assertEqual(simplify_string("Café crème à l'œuf"), "cafe-creme-a-l-oeuf")

        # Other complex examples
        self.assertEqual(
            simplify_string("Pâtés à l'œuf façon grand-mère"),
            "pates-a-l-oeuf-facon-grand-mere",
        )
        self.assertEqual(
            simplify_string("Crêpes sucrées aux œufs et à la crème"),
            "crepes-sucrees-aux-oeufs-et-a-la-creme",
        )

    def test_empty_string(self):
        """Test with empty string."""
        self.assertEqual(simplify_string(""), "")

    def test_string_without_special_chars(self):
        """Test with string without special characters."""
        self.assertEqual(simplify_string("tomate"), "tomate")
        self.assertEqual(simplify_string("carotte"), "carotte")
        self.assertEqual(simplify_string("pomme"), "pomme")

    def test_numbers_and_special_characters(self):
        """Test with numbers and special characters."""
        self.assertEqual(simplify_string("recette123"), "recette123")
        self.assertEqual(simplify_string("plat-principal"), "plat-principal")
        self.assertEqual(simplify_string("5-épices"), "5-epices")

    def test_multiple_spaces(self):
        """Test with multiple consecutive spaces."""
        self.assertEqual(simplify_string("tomate  cerise"), "tomate--cerise")
        self.assertEqual(simplify_string("crème   fraîche"), "creme---fraiche")

    def test_multiple_apostrophes(self):
        """Test with multiple apostrophes."""
        self.assertEqual(simplify_string("l'œuf's"), "l-oeuf-s")
        self.assertEqual(simplify_string("qu'est-ce qu'on"), "qu-est-ce-qu-on")

    def test_mixed_case_with_accents(self):
        """Test with mixed case and accents."""
        self.assertEqual(simplify_string("CaFÉ CrÈmE"), "cafe-creme")
        self.assertEqual(simplify_string("PÂTÉS À L'ŒUF"), "pates-a-l-oeuf")

    def test_unicode_characters(self):
        """Test with special Unicode characters."""
        # Characters with tilde
        self.assertEqual(simplify_string("niño"), "nino")
        self.assertEqual(simplify_string("piña"), "pina")

        # Characters with cedilla
        self.assertEqual(simplify_string("français"), "francais")

        # Characters with diaeresis
        self.assertEqual(simplify_string("naïf"), "naif")
        self.assertEqual(simplify_string("maïs"), "mais")

    def test_leading_trailing_spaces(self):
        """Test with leading and trailing spaces."""
        self.assertEqual(simplify_string(" café "), "-cafe-")
        self.assertEqual(simplify_string("  crème  "), "--creme--")

    def test_real_world_examples(self):
        """Test with real-world ingredient examples."""
        # Typical Marmiton ingredient examples
        self.assertEqual(simplify_string("Filet de bœuf"), "filet-de-boeuf")
        self.assertEqual(
            simplify_string("Crème fraîche épaisse"), "creme-fraiche-epaisse"
        )
        self.assertEqual(simplify_string("Pâte feuilletée"), "pate-feuilletee")
        self.assertEqual(simplify_string("Huile d'olive"), "huile-d-olive")
        self.assertEqual(simplify_string("Fromage râpé"), "fromage-rape")
        self.assertEqual(simplify_string("Œufs frais"), "oeufs-frais")
        self.assertEqual(simplify_string("Salade mélangée"), "salade-melangee")

    def test_edge_cases(self):
        """Test edge cases."""
        # String with only spaces
        self.assertEqual(simplify_string("   "), "---")

        # String with only apostrophes
        self.assertEqual(simplify_string("'''"), "---")

        # String with only characters to replace
        self.assertEqual(simplify_string("œæ ' "), "oeae---")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
