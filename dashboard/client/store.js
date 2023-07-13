import {createStore} from "vuex";
import axios from "axios";

const store = createStore({
    state: {
        // Trạng thái
        isDashboard: false,
        isAuthenticated: false
    },
    mutations: {
        // Các hàm để thay đổi trạng thái
        changeModeUI(state, sender) {
            if (sender?.isDashboard !== null) {
                state.isDashboard = sender.isDashboard;
            }
        },
        setAuthenticate(state, sender) {
            if (sender?.isAuthenticated !== null) {
                state.isAuthenticated = sender.isAuthenticated;
            }
        }
    },
    actions: {
        // Các hàm xử lý logic bất đồng
        changeModeUI(context, sender) {
            if (sender?.isDashboard !== null) {
                state.isDashboard = sender.isDashboard;
            }
            setTimeout(() => {
                context.commit('changeModeUI', sender)
            }, 1000);
        }
    },
    getters: {
        // Các hàm lấy dữ liệu từ trạng thái
    }
});

export default store