import pandas as pd
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
            
            # 👇 后台图表的横轴已经更新为你新加的“训练日期”了！
            chart_data = passenger_df.set_index("训练日期")["VAS疼痛评分"]
            st.line_chart(chart_data)
            
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