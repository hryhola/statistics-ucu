"""Task 4 report selection and layout; all saved output rows are retained."""
import ast
import re
SCAFFOLD="YOUR CODE"
def select_code(notebook, parts):
    """Select whole statements by prefix and carry the author's adjacent comments with them."""
    fragments = []
    provenance = []
    for cell_index, prefixes in parts:
        source = "".join(notebook["cells"][cell_index]["source"])
        lines = source.splitlines()
        nodes = [(ast.get_source_segment(source, node), node) for node in ast.parse(source).body]
        for prefix in prefixes:
            matches = [(code, node) for code, node in nodes if code.startswith(prefix)]
            assert len(matches) == 1, (cell_index, prefix)
            statement, node = matches[0]
            start = node.lineno - 1
            # Contiguous comment lines right above the statement (never the supplied scaffold)
            # and a trailing comment on its last line are part of the shown fragment.
            while start > 1 and lines[start - 1].lstrip().startswith("#") and SCAFFOLD not in lines[start - 1]:
                start -= 1
            code = "\n".join(lines[start:node.end_lineno])
            assert statement in code
            fragments.append(code)
            provenance.append({"cell": cell_index, "prefix": prefix, "statement": statement, "source": code})
    return "\n".join(fragments) + "\n", provenance


PART_TITLES = {1: '1. Lasso та Ridge', 2: '2. Дерева та ансамблі', 3: '3. Логістична регресія'}
# Original question cell, code cell, answer cell, descriptive title.
SECTIONS = {
1: [(5,6,7,'Концепція Lasso'), (8,9,10,'Масштабування та кодування'),
    (11,12,13,'Вибір штрафу Lasso'), (14,15,16,'Ridge та OLS')],
2: [(5,6,7,'Критерій поділу'), (11,12,13,'Порядкові та категоріальні ознаки'),
    (14,15,16,'Обмеження розміру CART'), (17,18,19,'Обрізання дерева'),
    (20,21,22,'Покращення в корені'), (23,24,25,'Важливості дерева та коефіцієнти'),
    (32,33,34,'Помилка ансамблів'), (35,36,37,'Час та важливості моделей')],
3: [(5,6,7,'Відбір за AIC'), (8,9,10,'Відношення шансів'),
    (11,12,13,'Значущість і знаки'), (14,15,16,'П’ять прогнозів'),
    (17,18,19,'Матриця помилок при 0.5'), (20,21,22,'ROC та поріг Юдена'),
    (23,24,25,'Класифікація з новим порогом')],
}
CODE = {
(1,9): ['numeric_pipe =','categorical_pipe =','preprocessor =','prepared =','Z_train =','Z_test =','feature_names =','scaler =','encoder =','fireplace_index ='],
(1,12): ['lasso_alphas =','lasso_cv =','lasso_cv.fit','lasso_search =','lasso_search.fit','lasso_model =','lasso_alpha =','path_alphas, coefficients, gaps ='],
(1,15): ['print("Прогноз:','ridge_alphas =','ridge_search =','ridge_search.fit','ridge_model =','ridge_alpha =','ols_model =','metrics =','for name, model','Z_centered =','rank =','sigma2 =','Z_pinv =','A_ridge =','var_ols =','var_ridge ='],
(2,12): ['quality_tree =','quality_tree.fit','quality_values =','print('],
(2,15): ['tree =','tree.fit','structure =','shown_tree =','scaler =','for node, feature'],
(2,18): ['print("Прогноз:','pruning_path =','pruning_rows =','for alpha in'],
(2,21): ['t =','left, right =','N, NL, NR =','I, IL, IR =','improvement =','root_feature =','root_threshold =','mask =','root_rss =','children_rss ='],
(2,24): ['lasso_search =','lasso_model =','ols_model =','importance =','tree_top10 =','manual_mdi =','for node, feature','manual_mdi /='],
(2,33): ['print("Прогноз:','ensemble_sizes =','ensembles =','curve_rows =','for name, model','curves =','plateau_rows =','for name, group'],
(2,36): ['print("Прогноз:','timing_rows =','for repeat in','timings =','timing_summary =','forest =','importance[','forest_mdi =','forest_mdi /=','mdi_difference =','final_importance ='],
(3,6): ['def fit_logit','selected =','model =','selection_rows =','fits_checked =','while selected:','beta_raw =','intercept_raw =','se_raw ='],  # the convergence diagnostics stay in the notebook; their table is shown
(3,9): ['lot_beta =','lot_ci =','lot_rows =','for increase in'],
(3,12): ['significant_positive =','significant_negative =','display(pd.crosstab'],
(3,15): ['sample_index =','sample_design =','sample_probabilities =','sample_results =','sample_results[','first_index =','first_values =','terms =','z_first =','print("Ймовірність'],
(3,18): ['valid_probabilities =','def threshold_metrics','matrix_default, metrics_default ='],
(3,21): ['fpr, tpr, thresholds =','auc_value =','youden =','finite =','best =','optimal_threshold ='],
(3,24): ['matrix_optimal, metrics_optimal =','comparison ='],
}
# Prefixes above may select several statements, in original source order.
# All non-empty outputs of these cells are included, with no row/column cuts.
FIGURES = {
(1,12): ('part1_lasso.png','Траєкторії коефіцієнтів і вибір штрафу Lasso.'),
(1,15): ('part1_ridge_ols.png','Крос-валідація Ridge, коефіцієнти та умовні дисперсії.'),
(2,15): ('part2_cart.png','Дерево CART із десятьма поділами. Пороги у початкових одиницях.'),
(2,18): ('part2_pruning.png','Розмір дерева та помилка при обрізанні.'),
(2,33): ('part2_ensemble_mse.png','Навчальна й валідаційна MSE залежно від кількості дерев.'),
(2,36): ('part2_forest_importance.png','П’ятнадцять найбільших важливостей випадкового лісу.'),
(3,18): ('part3_confusion_default.png','Матриця помилок при порозі 0.5.'),
(3,21): ('part3_roc.png','ROC-крива й обраний поріг Юдена.'),
(3,24): ('part3_confusion_comparison.png','Порівняння матриць помилок для двох порогів.'),
}
COMMON = ['df =','df.columns =','for column in','df["MSSubClass"] =','X =','y =','X_train, X_test, y_train, y_test =','numeric_columns =','categorical_columns =']
LOGIT_PREP = ['y =','excluded =','X =','X_train, X_valid, y_train, y_valid =','imputer =','raw_train =','raw_valid =','scaler =','Z_train =','Z_valid =','means =','scales =']
FRAME = ('# Вище: імпорти, налаштування та підготовка змінних.',
         '# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.')
# Page layout is kept here, not in generated LaTeX.
PAGE_BREAK_BEFORE_QUESTION = set()
PAGE_BREAK_BEFORE_ANSWER = set()
INTRO = '''Опціональні пункти 2.б, 2.з, 2.и пропущено.

Дані Ames Housing: 2930 продажів, SalePrice у доларах США, площі у квадратних
футах. Випадкове розбиття 80/20 із seed 42 дає 2344 навчальних і 586 відкладених
рядків, однакових для всіх частин; у частині 2 відкладені рядки називаємо
валідаційними, бо на них порівнюємо кілька моделей. Рівень значущості 0.05.

У частинах 1 і 2 вилучаємо Order, PID і GarageYrBlt; MSSubClass і текстові ознаки
кодуємо індикаторами з одним базовим рівнем, структурне NA є окремою категорією,
числові пропуски заповнюємо навчальною медіаною, числові ознаки стандартизуємо.
Усі перетворення навчаються лише на навчальній частині, штрафи вибираємо
5-блочною крос-валідацією. У частині 3 клас 1 означає SalePrice понад 130000
доларів; використовуємо лише числові ознаки, їх підготовку показано на початку
частини.'''

def answer_text(source):
    text = source.removeprefix('***Answer***').strip()
    # Interpretations carry no bold accents in the report.
    return re.sub(r'\*\*(.*?)\*\*', r'\1', text)

def chosen_code(notebook, cell, prefixes):
    source=''.join(notebook['cells'][cell]['source'])
    # Resolve loose editorial prefixes into exact, unique AST statements.
    statements=[ast.get_source_segment(source,n) for n in ast.parse(source).body]
    chosen=[s for s in statements if any(s.startswith(p) for p in prefixes)]
    for p in prefixes:
        assert any(s.startswith(p) for s in chosen), (cell,p)
    return select_code(notebook, [(cell,chosen)])

FIGURE_WIDTHS = {(3,18):0.65, (3,21):0.65, (3,24):0.88}
# Keep the full numerical substitution with its introductory sentence.
MARKDOWN_OUTPUT_NEEDSPACE = {(3,15): 530}
# Compact single-panel plots and adjacent small preparation tables avoid empty page tails.
FIGURE_WIDTHS.update({(3,18):0.52, (3,21):0.60, (3,24):0.85})
SIDE_BY_SIDE_OUTPUTS = {(1,3)}

# Shortened tables: (part, code cell, output index) -> kept rows/columns and the note printed under the table.
TABLE_CUTS = {
    (1,9,0): {'columns': [1,2,3], 'note': 'Скорочено: пропущено колонки «Середнє після стандартизації» (усі приблизно 0) та «SD після стандартизації» (усі дорівнюють 1).'},
    (1,12,3): {'rows': list(range(20)), 'note': 'Скорочено: із 126 ненульових коефіцієнтів Lasso показано 20 найбільших за модулем.'},
    (1,15,3): {'rows': list(range(34)), 'note': 'Скорочено: показано 34 числові ознаки; 260 рядків індикаторів категорій пропущено, їхні дисперсії входять у суми вище та в рисунок нижче.'},
    (2,36,4): {'rows': list(range(20)), 'note': 'Скорочено: із 294 ознак показано 20 з найбільшою MDI випадкового лісу; решта 274 мають меншу MDI.'},
}


def refs(text, part):
    """Write sub-task references as 1.г instead of (1)(г); the assignment statements are never changed."""
    text = re.sub(r"\((\d)\)\s*\(([а-я])\)", r"\1.\2", text)
    text = re.sub(r"(пункт[а-яі]*) \(([а-я])\)", lambda m: f"{m.group(1)} {part}.{m.group(2)}", text)
    text = re.sub(r"(частин[а-яі]*) \((\d)\)", r"\1 \2", text)
    return text
