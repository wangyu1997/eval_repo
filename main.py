import re
import sys

keywords = [
    'p1s', 'ctr', 'conv', 'conv_seq', 'cvr_p_on_all','cvr_p_on_clk','cvr_n_on_all','cvr_n_on_noclk','conv_APP','conv_APP_ctr','conv_SITE_PAGE','conv_SITE_PAGE_ctr','conv_AD_KWAI_SERIAL_PROMOTION','conv_AD_KWAI_SERIAL_PROMOTION_ctr','conv_MINI_APP_CAMPAIGN_TYPE','conv_MINI_APP_CAMPAIGN_TYPE_ctr','conv_PHOTO','conv_PHOTO_ctr','conv_AD_WX_MINI_APP','conv_AD_WX_MINI_APP_ctr','conv_AD_KWAI_FICTION_PROMOTION','conv_AD_KWAI_FICTION_PROMOTION_ctr', 'conv_p98', 'conv_p80', 'conv_p90'
]

def red_str(s):
    return "\033[1;31m%s\033[0m" % s


def green_str(s):
    return "\033[1;32m%s\033[0m" % s


def blue_str(s):
    return "\033[1;36m%s\033[0m" % s

p = re.compile(
    r"auc_(?P<name>[^: ]+) *: AUC=(?P<auc>[\d\.]+) UAUC=(?P<uauc>[\d\.]+) WUAUC=(?P<wuauc>[\d\.]+) .* InsNum=(?P<insNum>[\d]+) .* (LOSS=(?P<los>[\d\.]+)|MAE=(?P<mae>[\d\.]+)) .*(ActualCTR=(?P<actual_ctr>[\d\.]+)|ActualWatch=(?P<actual_watch>[\d\.]+)) .*(PredictedCTR=(?P<pred_ctr>[\d\.]+)|PredWatch=(?P<pred_watch>[\d\.]+))"
)


def f2arr(txt):
    l = {}
    for line in txt.strip('\n').strip().split('\n'):
        x = line.strip()
        m = p.search(x)
        if m is None:
            continue
        loss = m.group('name').strip()
        if loss not in keywords:
            continue
        auc = m.group('auc')
        uauc = m.group('uauc')
        wuauc = m.group('wuauc')
        ins_num = m.group('insNum')
        los = m.group('los')
        actual_ctr = m.group('actual_ctr')
        pred_ctr = m.group('pred_ctr')
        if not los:
            los = m.group('mae')
        if not actual_ctr:
            actual_ctr = m.group('actual_watch')
        if not pred_ctr:
            pred_ctr = m.group('pred_watch')
        l[loss] = (auc, uauc, wuauc, ins_num, los, actual_ctr, pred_ctr)
    return l


def diff_ctr(a, b):
    diff_a, diff_b = a * 100, b * 100
    str_a, str_b = '', ''
    if abs(a) > abs(b):
        str_b = '%spp' % red_str('%+.2f' % diff_b)
    else:
        str_b = '%spp' % green_str('%+.2f' % diff_b)
    return '%spp' % blue_str('%+.2f' % diff_a), str_b


def diff_pp(a, b, loss=False):
    diff = (b - a) * 100
    local_green_str, local_red_str = green_str, red_str
    if loss:
        local_green_str, local_red_str = red_str, green_str
    if diff > 0.0:
        return '%spp' % local_red_str('%+.2f' % diff)
    elif diff < 0.0:
        return '%spp' % local_green_str('%+.2f' % diff)
    else:
        return '%spp' % ('%+.2f' % diff)

def ins_bool(x, y):
    return x != y

def compare(base, exp):

    def ins(x, y):
        if x == y: return "no diff"
        else: return "%d/%d" % (x, y)

    a = f2arr(base)
    b = f2arr(exp)
    subs = []
    totals = []
    ended_loss = set()
    num = 0
    for loss in keywords:
        if loss in ended_loss:
            continue
        ended_loss.add(loss)
        if loss not in a or loss not in b:
            continue
        left = a[loss]
        right = b[loss]
        a_auc, a_uauc, a_wuauc, a_ins, a_los, a_ctr_diff = (float(
            left[0]), float(left[1]), float(left[2]), int(
                left[3]), float(left[4]), float(left[6]) - float(left[5]))
        b_auc, b_uauc, b_wuauc, b_ins, b_los, b_ctr_diff = (float(
            right[0]), float(right[1]), float(right[2]), int(
                right[3]), float(right[4]), float(right[6]) - float(right[5]))
        ctr_diff_a, ctr_diff_b = diff_ctr(a_ctr_diff, b_ctr_diff)
        # if ins_bool(a_ins, b_ins):
        #     print("sample number does not match...")
        # change to read
        print_loss = loss
        if loss.endswith('_ctr'):
            print_loss = 'ctr_' + loss[:-4]
        if loss == 'conv_p98' or loss == 'conv_APP':
              print('\n')
        print("%s  %s=%s %s=%s %s=%s %s=%s" % (
            print_loss.rjust(31),
            "AUC",
            "%.4f|%.4f(%s)" % (a_auc, b_auc, diff_pp(a_auc, b_auc)),
            "UAUC",
            "%.4f|%.4f(%s)" % (a_uauc, b_uauc, diff_pp(a_uauc, b_uauc)),
            "LOSS",
            "%.4f|%.4f(%s)" % (a_los, b_los, diff_pp(a_los, b_los, loss=True)),
            "pcoc",
            "%.4f|%.4f" % (float(left[6]) / float(left[5]), float(right[6]) / float(left[5]))
        ))


# 0923
base = """
stdout auc_p1s: AUC=0.880738 UAUC=0.773672 WUAUC=0.781849 UserNum=32232398 AllUserNum=130528250 InsNum=2258586753 MAE=0.157003 RMSE=0.281461 LOSS=0.254318 ActualCTR=0.124595 PredictedCTR=0.122778
stdout auc_ctr: AUC=0.920382 UAUC=0.777781 WUAUC=0.785215 UserNum=25274373 AllUserNum=130528250 InsNum=2258586753 MAE=0.041467 RMSE=0.145047 LOSS=0.084641 ActualCTR=0.033322 PredictedCTR=0.032851
stdout auc_conv: AUC=0.944084 UAUC=0.786456 WUAUC=0.810060 UserNum=7798209 AllUserNum=130528250 InsNum=2258586753 MAE=0.010929 RMSE=0.073156 LOSS=0.024136 ActualCTR=0.005980 PredictedCTR=0.006274
stdout auc_conv_seq: AUC=0.932028 UAUC=0.718252 WUAUC=0.739791 UserNum=7798209 AllUserNum=130528250 InsNum=2258586753 MAE=0.010790 RMSE=0.074285 LOSS=0.025612 ActualCTR=0.005980 PredictedCTR=0.005707
stdout auc_conv_p98: AUC=0.940208 UAUC=0.776960 WUAUC=0.797110 UserNum=7450911 AllUserNum=119763146 InsNum=1857579751 MAE=0.012883 RMSE=0.079424 LOSS=0.028082 ActualCTR=0.007064 PredictedCTR=0.007414
stdout auc_conv_p80: AUC=0.945232 UAUC=0.780543 WUAUC=0.804491 UserNum=7040690 AllUserNum=130528250 InsNum=2258586753 MAE=0.009340 RMSE=0.068393 LOSS=0.021497 ActualCTR=0.005136 PredictedCTR=0.005135
stdout auc_conv_p90: AUC=0.944906 UAUC=0.782074 WUAUC=0.805555 UserNum=7494646 AllUserNum=130528250 InsNum=2258586753 MAE=0.010103 RMSE=0.071165 LOSS=0.022988 ActualCTR=0.005609 PredictedCTR=0.005600
"""

exp = """
stdout auc_p1s: AUC=0.880727 UAUC=0.773734 WUAUC=0.781912 UserNum=32232398 AllUserNum=130528250 InsNum=2258586753 MAE=0.157810 RMSE=0.281463 LOSS=0.254307 ActualCTR=0.124595 PredictedCTR=0.123383
stdout auc_ctr: AUC=0.920528 UAUC=0.777322 WUAUC=0.784843 UserNum=25274373 AllUserNum=130528250 InsNum=2258586753 MAE=0.040818 RMSE=0.144967 LOSS=0.084578 ActualCTR=0.033322 PredictedCTR=0.031788
stdout auc_conv: AUC=0.944134 UAUC=0.786573 WUAUC=0.810212 UserNum=7798209 AllUserNum=130528250 InsNum=2258586753 MAE=0.010720 RMSE=0.073141 LOSS=0.024125 ActualCTR=0.005980 PredictedCTR=0.006045
stdout auc_conv_seq: AUC=0.932008 UAUC=0.717090 WUAUC=0.738743 UserNum=7798209 AllUserNum=130528250 InsNum=2258586753 MAE=0.010817 RMSE=0.074288 LOSS=0.025615 ActualCTR=0.005980 PredictedCTR=0.005749
stdout auc_conv_p98: AUC=0.940255 UAUC=0.777090 WUAUC=0.797285 UserNum=7450911 AllUserNum=119763146 InsNum=1857579751 MAE=0.012643 RMSE=0.079407 LOSS=0.028069 ActualCTR=0.007064 PredictedCTR=0.007149
stdout auc_conv_p80: AUC=0.945252 UAUC=0.780854 WUAUC=0.804867 UserNum=7040690 AllUserNum=130528250 InsNum=2258586753 MAE=0.009170 RMSE=0.068387 LOSS=0.021499 ActualCTR=0.005136 PredictedCTR=0.004952
stdout auc_conv_p90: AUC=0.944937 UAUC=0.782290 WUAUC=0.805853 UserNum=7494646 AllUserNum=130528250 InsNum=2258586753 MAE=0.009915 RMSE=0.071159 LOSS=0.022990 ActualCTR=0.005609 PredictedCTR=0.005394
"""

compare(base, exp)
