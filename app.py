import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
from pathlib import Path

# ---------- 0、系统底层配置 ----------
REHAB_CSV_PATH = Path(__file__).parent / "rehab_data.csv"

# ==========================================
# 🚀 核心装修：在网页最顶端建立s两个折叠空间
# ==========================================
tab1, tab2 = st.tabs(["🧍 居家康复打卡站", "👨‍⚕️ 主治医师数据后台"])

# ==========================================
# 空间一：患者前台（所有内容藏在 tab1 里）
# ==========================================
with tab1:
    st.markdown("### 📋 今日康复处方")
    st.markdown("- **动作：** 靠墙静蹲 (Wall Sit)")
    st.markdown("- **容量：** 3 组，每组 45 秒")
    st.video("https://www.youtube.com/watch?v=y-wV4Venusw")
    st.divider()

    st.subheader("📝 今日打卡")
    patient_name = st.text_input("患者姓名", placeholder="请输入您的姓名")
    
    # 👇 完美植入的日历功能
    record_date = st.date_input("📅 选择训练日期")
    
    actual_sets = st.number_input("实际完成组数", min_value=0, step=1, value=0)
    vas_score = st.slider("VAS 疼痛评分（0-10 分）", min_value=0, max_value=10, value=0)
    submitted = st.button("提交今日打卡", type="primary", use_container_width=True)

    if submitted:
        # 1. 记账
        check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_record = {
            "训练日期": str(record_date),  # 👈 新加入的日期列
            "患者姓名": patient_name,
            "实际组数": actual_sets,
            "VAS疼痛评分": vas_score,
            "打卡时间": check_in_time,
        }
        new_row_df = pd.DataFrame([new_record])
        
        if REHAB_CSV_PATH.exists():
            existing_df = pd.read_csv(REHAB_CSV_PATH, encoding="utf-8-sig")
            combined_df = pd.concat([existing_df, new_row_df], ignore_index=True)
            combined_df.to_csv(REHAB_CSV_PATH, index=False, encoding="utf-8-sig")
        else:
            new_row_df.to_csv(REHAB_CSV_PATH, index=False, encoding="utf-8-sig")
            
        st.info("💾 您的打卡数据已成功记入康复档案表格！")

        # 2. 警报与奖励逻辑
        if vas_score >= 5 or actual_sets < 3:
            st.error("🚨 警告：未达标或疼痛过高！请立刻停止训练，冰敷并联系主治医师！")
        else:
            st.success("✅ 恭喜完成！状态极佳，明天我们将增加一点抗阻力！")
            st.toast("🎉 伟大的坚持！你今天的自律战胜了疼痛！", icon="🔥")
            st.balloons()

# ==========================================
# 空间二：医生后台（加装数字防盗门）
# ==========================================
with tab2:
    st.subheader("👨‍⚕️ 医师身份验证")
    
    doctor_password = st.text_input("🔒 请输入主治医师专属密码以解锁档案：", type="password")
    
    if doctor_password == "admin123":
        st.success("✅ 身份确认。欢迎回来，主治医师。")
        st.divider()
        
        st.subheader("📊 历史康复趋势检索")
        if REHAB_CSV_PATH.exists():
            df = pd.read_csv(REHAB_CSV_PATH, encoding="utf-8-sig")
            patient_list = df["患者姓名"].unique()
            selected_patient = st.selectbox("🔍 请选择要查看的患者档案", options=patient_list)
            st.markdown(f"正在展示 **{selected_patient}** 的专属康复曲线：")
            
            passenger_df = df[df["患者姓名"] == selected_patient]
            
            # --- 👇 进阶可视化：Matplotlib 医疗级图表 👇 ---
            # 1. 准备数据：把日期和疼痛分数分别提取出来变成列表
            dates = passenger_df["训练日期"].tolist()
            scores = passenger_df["VAS疼痛评分"].tolist()
            
            # 2. 召唤画布和画笔（figsize=(10, 4) 控制图表的长宽比例）
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # 3. 画出核心折线
            ax.plot(dates, scores, marker='o', color='#1f77b4', linewidth=2, markersize=8)
            
            # 4. 🌟 点睛之笔：画出浅红色的“危险预警区”
            ax.axhspan(ymin=5, ymax=10, color='red', alpha=0.15, label='高危疼痛区 (VAS 5-10)')

            # +++++++++++++++++++++++++++++++++++++++++++
            # 👇 今日新增模块：自动追踪最高疼痛极值 👇
            
            # 第一步：找出这堆分数里的最高分 (寻峰)
            max_score = max(scores)
            
            # 第二步：找出这个最高分在列表里的位置，并揪出对应的日期 (定位)
            max_index = scores.index(max_score)
            max_date = dates[max_index]
            
            # 第三步：指挥画笔，在这个坐标画一个带有红箭头的提示框
            ax.annotate(f"Peak Pain: {max_score}", 
                        xy=(max_date, max_score),            # 箭头尖端指着的目标坐标
                        xytext=(max_date, max_score + 1.5),  # 文字框悬浮的坐标（比最高点再高1.5分）
                        arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=8), # 定制红色箭头
                        ha='center', color='red', fontweight='bold') # 文字居中、标红、加粗
                        
            # 👆 今日新增模块结束 👆
            # +++++++++++++++++++++++++++++++++++++++++++

            # 5. 装修图表边界和文字
            ax.set_ylim(0, 10.5)
            ax.set_ylabel("VAS Pain Score") # Y轴贴上标签
            ax.set_title(f"患者 {selected_patient} 的疼痛趋势分析") # 加上霸气的标题
            ax.grid(True, linestyle='--', alpha=0.6) # 加上虚线网格，看起来更专业
            ax.legend(loc="upper left") # 在左上角显示图例（解释红框是什么）
            
            # 6. 把画好的神作挂到 Streamlit 网页上
            st.pyplot(fig)
            # --- 👆 可视化手术结束 👆 ---
            
            st.divider() 
            
            # 👇 --- 新增手术：依从性雷达（患者自律性分析） --- 👇
            st.subheader("🎯 患者依从性分析")
            
            # 1. 算总数：患者总共打卡了几天？
            total_days = len(passenger_df) 
            
            # 2. 算达标数：只有“实际组数”大于等于 3 的，才算真正的 Good Boy
            good_days = len(passenger_df[passenger_df["实际组数"] >= 3])
            
            if total_days > 0:
                # 3. 算百分比：达标率 = (达标天数 / 总天数) * 100
                compliance_rate = (good_days / total_days) * 100
                
                # 4. 酷炫的前端展示：把页面切成两列，放上仪表盘
                col1, col2 = st.columns(2)
                col1.metric(label="累计打卡天数", value=f"{total_days} 天")
                col2.metric(label="高质量达标率", value=f"{compliance_rate:.1f}%", delta=f"{good_days} 天达标")
                
                # 5. 临床智能预警
                if compliance_rate >= 80:
                    st.success("🌟 极佳的依从性！患者高度自律，康复进度非常有保障。")
                elif compliance_rate >= 60:
                    st.info("🔄 依从性尚可，建议在复诊时给予正向鼓励。")
                else:
                    st.warning("⚠️ 警报：高质量完成率过低！患者极可能存在抗拒心理或严重动作代偿，需立刻介入干预！")
            # 👆 --- 新增手术结束 --- 👆

            st.divider() 
            st.subheader("🧠 AI 助理诊断报告")
            if len(passenger_df) >= 3:
                recent_3_records = passenger_df.tail(3)
                avg_pain = recent_3_records["VAS疼痛评分"].mean()
                st.markdown(f"**该患者最近 3 次的平均疼痛指数为： {avg_pain:.1f} 分**")
                
                if avg_pain >= 5:
                    st.error("🚨 警报：近期平均疼痛值处于高位！建议立刻介入，检查动作代偿或降低训练容量！")
                elif avg_pain <= 2:
                    st.success("✅ 状态极佳：疼痛已显著缓解，可以考虑增加抗阻力训练！")
                else:
                    st.info("🔄 稳步恢复中：疼痛处于中等可控范围。")
            else:
                st.warning("⚠️ 该患者打卡次数不足 3 次，数据量不足，暂无法生成智能诊断报告。")
        else:
            st.info("暂无历史打卡记录。这里是医生的专属数据看板。")
            
    elif doctor_password != "":
        st.error("❌ 密码错误！您无权访问患者隐私数据！")