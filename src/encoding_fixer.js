// encoding_fixer.js - Correction encodage UTF-8 corrompu
const fs = require('fs');
const path = require('path');

/**
 * Mapping des caractères UTF-8 corrompus → caractères corrects
 */
const ENCODING_FIXES = {
    // Voyelles accentuées
    'Ã©': 'é',
    'Ã¨': 'è',
    'Ãª': 'ê',
    'Ã ': 'à',
    'Ã¢': 'â',
    'Ã´': 'ô',
    'Ã®': 'î',
    'Ã»': 'û',
    'Ã¹': 'ù',

    // Majuscules accentuées
    'Ã‰': 'É',
    'Ãˆ': 'È',
    'ÃŠ': 'Ê',
    'Ã€': 'À',
    'Ã‚': 'Â',
    'Ã"': 'Ô',
    'ÃŽ': 'Î',
    'Ã›': 'Û',
    'Ã™': 'Ù',

    // Cédille
    'Ã§': 'ç',
    'Ã‡': 'Ç',

    // Ligatures
    'Å"': 'œ',
    'Å ': 'Œ',

    // Guillemets et ponctuation
    '\u00C2\u00AB': '«',
    '\u00C2\u00BB': '»',
    '\u00E2\u0080\u0099': "'",
    '\u00E2\u0080\u009C': '"',
    '\u00E2\u0080\u009D': '"',
    '\u00E2\u0080\u0094': '—',
    '\u00E2\u0080\u0093': '–',
    '\u00E2\u0080\u00A6': '…'
};

/**
 * Fixe l'encodage d'une chaîne de caractères
 */
function fixEncoding(text) {
    let fixed = text;

    for (const [corrupt, correct] of Object.entries(ENCODING_FIXES)) {
        fixed = fixed.split(corrupt).join(correct);
    }

    return fixed;
}

/**
 * Traite un fichier et le sauvegarde corrigé
 */
function fixFile(inputPath, outputPath) {
    console.log(`📖 Lecture de ${path.basename(inputPath)}...`);

    const content = fs.readFileSync(inputPath, 'utf8');
    const fixed = fixEncoding(content);

    // Compter les corrections
    const corrections = Object.keys(ENCODING_FIXES).filter(corrupt =>
        content.includes(corrupt)
    ).length;

    fs.writeFileSync(outputPath, fixed, 'utf8');

    console.log(`✅ ${path.basename(outputPath)} : ${corrections} types de corrections appliquées`);

    return { corrections, size: Buffer.byteLength(fixed, 'utf8') };
}

/**
 * Traite tous les fichiers d'un dossier
 */
function fixDirectory(inputDir, outputDir) {
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    const files = fs.readdirSync(inputDir)
        .filter(f => f.endsWith('.md'));

    console.log(`\n🔧 Correction encodage UTF-8\n${'='.repeat(40)}\n`);

    let totalCorrections = 0;

    for (const file of files) {
        const inputPath = path.join(inputDir, file);
        const outputPath = path.join(outputDir, file.replace('.md', '_clean.md'));

        const result = fixFile(inputPath, outputPath);
        totalCorrections += result.corrections;
    }

    console.log(`\n✨ Total : ${totalCorrections} types de corrections sur ${files.length} fichiers\n`);
}

// Export pour usage en module
module.exports = { fixEncoding, fixFile, fixDirectory };

// Usage CLI
if (require.main === module) {
    const inputDir = path.join(__dirname, '../../RAG');
    const outputDir = path.join(__dirname, '../RAG_clean');

    fixDirectory(inputDir, outputDir);
}
