"""Editorial selections: essential notebook statements and saved outputs for the report."""
import ast
import re

SCAFFOLD = "YOUR CODE"  # supplied scaffold comments are never carried into the report
CODE = {
    (5, 5): [(5, ["numeric_class =", "formula_class =", "df_category =", "category_class ="])],
    (5, 8): [(8, ["scatter_columns =", "units =", "fig, axes =", "for ax, column", "axes.flat[-1].axis", "plt.show()"] )],
    (5, 11): [(11, ["simple_model =", "print(simple_model.summary())", "beta_1 =", "se_1 =", "t_1 =", "p_1 =", "assert np.isclose(t_1", "assert np.isclose(p_1", "display(pd.Series"])],
    (5, 14): [(14, ["category_order =", "groups =", "blocks =", "for column in category_order", "X_encoded =", "def design_matrix", "X_full =", "y =", "full_model =", "dummy_names =", "q, k =", "positions =", "R =", "R[np.arange", "r =", "f_result ="])],
    (5, 17): [(17, ["full_log_model =", "first_dummy =", "terms =", "gamma ="])],
    (5, 20): [(20, ["ci =", "jb =", "fig, axes =", "axes[0].hist", "sm.qqplot", "plt.show()"] )],
    (5, 23): [(23, ["def backward_bic", "selected_model, selected_terms, history =", "X_selected ="])],
    (5, 26): [(26, ["influence =", "with np.errstate", "exact_fit =", "cooks[exact_fit] =", "student[exact_fit] =", "top_cook =", "without_top ="])],
    (5, 29): [(29, ["masked_index =", "true_lotarea =", "df_missing =", 'df_missing["LotArea"] =', 'df_missing.loc[masked_index', "impute_columns =", "median_filled =", "median_filled[impute_columns] =", "iterative_filled =", "iterative_filled[impute_columns] ="])],
    (5, 32): [(32, ["level_model =", "log_model =", "n_obs =", "assert (level_model", "aux_level =", "aux_log =", "comparison_rows =", "for name, auxiliary", "jacobian ="])],
    (5, 35): [(35, ["X_full_cv =", "X_selected_cv =", "splitters =", "models =", "cv_rows, cv_errors =", "for scheme, splitter", "cv_results ="])],
    (6, 6): [(4, ["from scipy.optimize", "df_500 =", "x =", "y =", "n ="]), (6, ["linear_model =", "linear_pred =", "years =", "fig, ax =", "ax.scatter", "ax.plot", "plt.show()"] )],
    (6, 9): [(9, ["YEAR_0 =", "def exponential", "log_fit =", "p0 =", "params, pcov =", "a_hat, b_hat =", "exp_pred =", "def r_squared", "def mse"])],
    (6, 12): [(12, ["t =", "J =", "s2 =", "se =", "z =", "residuals =", "jb ="])],
    (6, 15): [(2, ["import warnings"]), (15, ["def exponential_raw", "with warnings.catch_warnings", "raw_params, raw_cov =", "raw_se =", "features =", "categorical =", "X_all =", "complete =", "X_complete ="])],
}
# Initial cells are used only once, before the first task. Imports stay in the notebooks.
COMMON = [(2, ["SEED =", "ALPHA =", "rng ="]),
          (3, ["DATA_PATH =", "df =", "df.columns =", "text_columns =", "for column in text_columns", "categorical =", "excluded =", "numeric =", "analysis ="])]
# Unlisted output objects are omitted. Every selected object comes from an executed cell.
OUTPUTS = {
    (5, 5): [0, 1, 2, 3, 4], (5, 8): [1, 2, 3, 4, 0], (5, 11): [0, 1],
    (5, 14): [0, 2], (5, 17): [0, 1, 2], (5, 20): [2, 0, 1],
    (5, 23): [0, 1, 2], (5, 26): [0, 1, 2, 3, 4, 5, 6],
    (5, 29): [0, 1, 2, 3], (5, 32): [2, 0, 1], (5, 35): [0, 1, 2, 3],
    (6, 6): [0, 1, 2, 3], (6, 9): [0, 1, 2, 3, 4],
    (6, 12): [0, 1, 2, 3], (6, 15): [0, 1, 2],
}
# Column indexes include the row-label column. Row indexes refer to saved HTML rows.
# Every cut is marked in the report as a shortened output.
TABLE_CUTS = {
    (5, 23, 0): {"rows": [0, 1, 2, 3, 4, 44, 45, 46, 47, 48], "ellipsis_after": 5},
}
# Each shortened output gets a specific note right under it: what is shown and what is left out.
NOTES = {
    (5, 23, 0): "Скорочено: з 49 рядків історії показано кроки 0–4 і 44–48; рядок «…» позначає пропущені кроки 5–43.",
}
# Interpretations that start on a new page: keyed by the code cell they follow.
PAGE_BREAK_BEFORE_ANSWER = {(5, 20)}
# Sub-task headings that start on a new page: (problem, heading label).
PAGE_BREAK_BEFORE_QUESTION = {(5, "(7)")}
# Comments that frame each shortened listing (one line each): what the notebook does before and after.
FRAME = {
    "common": ("# Вище: імпорти бібліотек, шляхи до файлів, налаштування графіків.",
               "# Далі: розмір df, кількість пропусків і структурних рівнів \"NA\"."),
    (5, 5): ("# Вище: print типу MSSubClass (вивід нижче).",
             "# Далі: assert рівності прогнозів, збирання таблиць (виводи нижче), графік."),
    (5, 8): (None, "# Далі: збереження рисунка; describe(), нулі, кореляції, групи років (виводи нижче)."),
    (5, 11): (None, None),
    (5, 14): ("# Вище: assert, що TotalBsmtSF і GrLivArea є сумами інших площ.",
              "# Далі: assert рангу, модель без MSSubClass, ручний F і assert збігу з f_test()."),
    (5, 17): (None, "# Далі: збирання таблиць коефіцієнтів і років побудови класів 20 і 30 (виводи нижче)."),
    (5, 20): (None, "# Далі: ручний перерахунок інтервалу з assert, підписи осей, збереження рисунка."),
    (5, 23): (None, "# Далі: assert рангу і локального оптимуму BIC; друк історії та списку змінних."),
    (5, 26): (None, "# Далі: assert суми важелів, пошук рідкісних рівнів для h = 1, таблиці, графіки."),
    (5, 29): (None, "# Далі: таблиці порівняння з істинними значеннями; assert, що змінено лише пропуски."),
    (5, 32): (None, "# Далі: збирання таблиць тесту та AIC/BIC з поправкою (виводи нижче)."),
    (5, 35): (None, "# Далі: assert збігу LinearRegression і OLS, найбільші помилки LOO, графік."),
    (6, 6): (None, "# Далі: describe(), роки продажу, таблиці оцінок і залишків, оформлення графіка."),
    (6, 9): (None, "# Далі: assert R² лінійної моделі, таблиці порівняння, контрольні роки, графік."),
    (6, 12): (None, "# Далі: assert pcov = s²(JᵀJ)⁻¹, таблиця оцінок, розкид залишків за періодами, графік."),
    (6, 15): (None, "# Далі: друк попереджень, таблиці порівняння параметризацій і розмірів матриці."),
}


def frame_code(key, code):
    before, after = FRAME[key]
    return "".join([before + "\n" if before else "", code, after + "\n" if after else ""])
INTRO = {
    5: """Дані Ames Housing містять 2930 продажів. SalePrice вимірюється в доларах США, площі у квадратних футах. Рівень значущості 0.05, початкове значення генератора 42. Розрахунки виконано в numpy, pandas, scipy, statsmodels і scikit-learn; імпорти та оформлення графіків наведено лише в notebook.

У множинних регресіях використовуємо 2414 повних спостережень. MSSubClass і текстові ознаки кодуємо фіктивними змінними; базовий рівень найчастіший. Не включаємо ідентифікатори Order та PID, GarageYrBlt (не визначений без гаража), а також TotalBsmtSF і GrLivArea, які є точними сумами інших площ. Категоріальні значення NA зберігаємо як окремі рівні.""",
    6: """За умовою використовуємо лише перші 500 продажів та пояснюємо SalePrice через YearBuilt. У цих двох колонках немає пропусків. Файл упорядкований за роком продажу, тому ця підвибірка містить лише продажі 2009–2010 років і не є випадковою.""",
}


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


def answer_text(source):
    text = source.removeprefix("***Answer***").strip()
    # Do not duplicate numerical output tables in the interpretation.
    text = re.sub(r"(?m)(?:^\|.*\n?)+", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    for sentence in [
        "Код перевіряє, що жодне наступне вилучення не покращує BIC.",
        "Ми перевірили цю формулу (`assert`). ",
        " (перевірено `assert`)", " (перевірено в коді)",
    ]:
        text = text.replace(sentence, "")
    text = text.replace("Наступні за впливом Order 514 і 1761 ($D=0.22$ і $0.18$).", "")
    old = "Сім із них містять унікальний рівень категорії: `KitchenQual=Po`, `RoofMatl=Membran`, `ClyTile`, `Roll`, `MasVnrType=CBlock`, `MiscFeature=Elev`, `TenC`. Восьмий, Order 2358, має `PoolQC=Fa`: таких продажів два, але інший уже виділено індикатором `TenC`."
    new = "Причина в рідкісних категоріях. Наприклад, Order 1499 є єдиним продажем із `RoofMatl=ClyTile`, а Order 2181 із `MiscFeature=Elev`. Order 2358 має `PoolQC=Fa`: таких продажів два, але інший уже виділено унікальним індикатором `TenC`."
    return text.replace(old, new)
