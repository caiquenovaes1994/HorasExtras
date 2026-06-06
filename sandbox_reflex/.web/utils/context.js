import { createContext, useContext, useMemo, useReducer, useState, createElement, useEffect } from "react"
import { applyDelta, ReflexEvent, hydrateClientStorage, useEventLoop, refs } from "$/utils/state"
import { jsx } from "@emotion/react";

export const initialState = {"reflex___state____state": {"is_hydrated_rx_state_": false, "router_rx_state_": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "cookie": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": "", "raw_headers": {}}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}, "url": {"scheme": "", "netloc": "", "origin": "://", "path": "", "query": "", "query_parameters": {}, "fragment": "", "href": ""}, "route_id": ""}}, "reflex___state____state.reflex___istate___shared____shared_state_base_internal": {}, "reflex___state____state.reflex___state____frontend_event_exception_state": {}, "reflex___state____state.reflex___state____on_load_internal_state": {}, "reflex___state____state.reflex___state____update_vars_internal_state": {}, "reflex___state____state.sandbox_reflex___state____auth_state": {"auth_token_rx_state_": "", "is_authenticated_rx_state_": false, "is_profile_modal_open_rx_state_": false, "login_error_rx_state_": "", "must_change_password_rx_state_": false, "needs_lgpd_acceptance_rx_state_": false, "p_new_password_rx_state_": "", "p_nome_rx_state_": "", "p_valor_base_rx_state_": "", "show_policy_rx_state_": false, "user_info_rx_state_": {"nome": "", "username": "", "perfil": "", "aceitou_termos": true}}, "reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state": {"active_tab_rx_state_": "historico", "ano_ref_rx_state_": "2024", "filtro_plantonista_rx_state_": "TODOS", "ganhos_estimados_rx_state_": "R$ 0,00", "is_all_selected_rx_state_": false, "is_generating_pdf_rx_state_": false, "media_por_chamado_rx_state_": "0h 00m", "mes_ref_rx_state_": "JANEIRO", "opcoes_plantonistas_rx_state_": ["TODOS"], "registros_agrupados_rx_state_": [], "selected_records_rx_state_": [], "show_empty_equipe_alert_rx_state_": false, "show_plantonista_alert_rx_state_": false, "total_chamados_rx_state_": 0, "total_horas_100_rx_state_": "00:00", "total_horas_100_td_rx_state_": "0:00:00", "total_horas_50_rx_state_": "00:00", "total_horas_50_td_rx_state_": "0:00:00"}, "reflex___state____state.sandbox_reflex___state_form____form_state": {"error_message_rx_state_": "", "f_caso_rx_state_": "", "f_data_rx_state_": "", "f_hotel_rx_state_": "", "f_inicio_rx_state_": "", "f_motivo_rx_state_": "", "f_obs_rx_state_": "", "f_termino_rx_state_": "", "hoteis_opts_rx_state_": [], "is_modal_open_rx_state_": false, "is_view_only_rx_state_": false, "record_id_rx_state_": -1}, "reflex___state____state.sandbox_reflex___state_hoteis____hotel_state": {"filtered_hoteis_rx_state_": [], "h_nome_rx_state_": "", "h_original_rid_rx_state_": "", "h_rid_rx_state_": "", "hoteis_rx_state_": [], "is_modal_open_rx_state_": false, "search_query_rx_state_": "", "solicitacoes_rx_state_": []}, "reflex___state____state.sandbox_reflex___state_usuarios____usuario_state": {"is_modal_open_rx_state_": false, "u_id_rx_state_": -1, "u_nome_rx_state_": "", "u_perfil_rx_state_": "USER", "u_username_rx_state_": "", "usuarios_rx_state_": []}}

export const defaultColorMode = "dark"
export const ColorModeContext = createContext({
  colorMode: defaultColorMode,
  resolvedColorMode: defaultColorMode === "dark" ? "dark" : "light",
  toggleColorMode: () => {},
  setColorMode: () => {},
});
export const UploadFilesContext = createContext(null);
export const DispatchContext = createContext(null);
export const StateContexts = {reflex___state____state: createContext(null),reflex___state____state__reflex___istate___shared____shared_state_base_internal: createContext(null),reflex___state____state__reflex___state____frontend_event_exception_state: createContext(null),reflex___state____state__reflex___state____on_load_internal_state: createContext(null),reflex___state____state__reflex___state____update_vars_internal_state: createContext(null),reflex___state____state__sandbox_reflex___state____auth_state: createContext(null),reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state: createContext(null),reflex___state____state__sandbox_reflex___state_form____form_state: createContext(null),reflex___state____state__sandbox_reflex___state_hoteis____hotel_state: createContext(null),reflex___state____state__sandbox_reflex___state_usuarios____usuario_state: createContext(null),};
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {"reflex___state____state.sandbox_reflex___state____auth_state.auth_token_rx_state_": {"path": "/", "maxAge": 86400, "sameSite": "lax"}}, "local_storage": {}, "session_storage": {}}


export const state_name = "reflex___state____state"

export const exception_state_name = "reflex___state____state.reflex___state____frontend_event_exception_state"

// These events are triggered on initial load and each page navigation.
export const onLoadInternalEvent = () => {
    const internal_events = [];

    // Get tracked cookie and local storage vars to send to the backend.
    const client_storage_vars = hydrateClientStorage(clientStorage);
    // But only send the vars if any are actually set in the browser.
    if (client_storage_vars && Object.keys(client_storage_vars).length !== 0) {
        internal_events.push(
            ReflexEvent(
                'reflex___state____state.reflex___state____update_vars_internal_state.update_vars_internal',
                {vars: client_storage_vars},
            ),
        );
    }

    // `on_load_internal` triggers the correct on_load event(s) for the current page.
    // If the page does not define any on_load event, this will just set `is_hydrated = true`.
    internal_events.push(ReflexEvent('reflex___state____state.reflex___state____on_load_internal_state.on_load_internal'));

    return internal_events;
}

// The following events are sent when the websocket connects or reconnects.
export const initialEvents = () => [
    ReflexEvent('reflex___state____state.hydrate'),
    ...onLoadInternalEvent()
]
    

export const isDevMode = true;

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return createElement(
    UploadFilesContext.Provider,
    { value: [filesById, setFilesById] },
    children
  );
}

export function ClientSide(component) {
  return ({ children, ...props }) => {
    const [Component, setComponent] = useState(null);
    useEffect(() => {
      async function load() {
        const comp = await component();
        setComponent(() => comp);
      }
      load();
    }, []);
    return Component ? jsx(Component, props, children) : null;
  };
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEvents, connectErrors] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  return createElement(
    EventLoopContext.Provider,
    { value: [addEvents, connectErrors] },
    children
  );
}

export function StateProvider({ children }) {
  const [reflex___state____state, dispatch_reflex___state____state] = useReducer(applyDelta, initialState["reflex___state____state"])
const [reflex___state____state__reflex___istate___shared____shared_state_base_internal, dispatch_reflex___state____state__reflex___istate___shared____shared_state_base_internal] = useReducer(applyDelta, initialState["reflex___state____state.reflex___istate___shared____shared_state_base_internal"])
const [reflex___state____state__reflex___state____frontend_event_exception_state, dispatch_reflex___state____state__reflex___state____frontend_event_exception_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____frontend_event_exception_state"])
const [reflex___state____state__reflex___state____on_load_internal_state, dispatch_reflex___state____state__reflex___state____on_load_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____on_load_internal_state"])
const [reflex___state____state__reflex___state____update_vars_internal_state, dispatch_reflex___state____state__reflex___state____update_vars_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____update_vars_internal_state"])
const [reflex___state____state__sandbox_reflex___state____auth_state, dispatch_reflex___state____state__sandbox_reflex___state____auth_state] = useReducer(applyDelta, initialState["reflex___state____state.sandbox_reflex___state____auth_state"])
const [reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state, dispatch_reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state] = useReducer(applyDelta, initialState["reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state"])
const [reflex___state____state__sandbox_reflex___state_form____form_state, dispatch_reflex___state____state__sandbox_reflex___state_form____form_state] = useReducer(applyDelta, initialState["reflex___state____state.sandbox_reflex___state_form____form_state"])
const [reflex___state____state__sandbox_reflex___state_hoteis____hotel_state, dispatch_reflex___state____state__sandbox_reflex___state_hoteis____hotel_state] = useReducer(applyDelta, initialState["reflex___state____state.sandbox_reflex___state_hoteis____hotel_state"])
const [reflex___state____state__sandbox_reflex___state_usuarios____usuario_state, dispatch_reflex___state____state__sandbox_reflex___state_usuarios____usuario_state] = useReducer(applyDelta, initialState["reflex___state____state.sandbox_reflex___state_usuarios____usuario_state"])
  const dispatchers = useMemo(() => {
    return {
      "reflex___state____state": dispatch_reflex___state____state,
"reflex___state____state.reflex___istate___shared____shared_state_base_internal": dispatch_reflex___state____state__reflex___istate___shared____shared_state_base_internal,
"reflex___state____state.reflex___state____frontend_event_exception_state": dispatch_reflex___state____state__reflex___state____frontend_event_exception_state,
"reflex___state____state.reflex___state____on_load_internal_state": dispatch_reflex___state____state__reflex___state____on_load_internal_state,
"reflex___state____state.reflex___state____update_vars_internal_state": dispatch_reflex___state____state__reflex___state____update_vars_internal_state,
"reflex___state____state.sandbox_reflex___state____auth_state": dispatch_reflex___state____state__sandbox_reflex___state____auth_state,
"reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state": dispatch_reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state,
"reflex___state____state.sandbox_reflex___state_form____form_state": dispatch_reflex___state____state__sandbox_reflex___state_form____form_state,
"reflex___state____state.sandbox_reflex___state_hoteis____hotel_state": dispatch_reflex___state____state__sandbox_reflex___state_hoteis____hotel_state,
"reflex___state____state.sandbox_reflex___state_usuarios____usuario_state": dispatch_reflex___state____state__sandbox_reflex___state_usuarios____usuario_state,
    }
  }, [])

  return (
    createElement(StateContexts.reflex___state____state,{value: reflex___state____state},
createElement(StateContexts.reflex___state____state__reflex___istate___shared____shared_state_base_internal,{value: reflex___state____state__reflex___istate___shared____shared_state_base_internal},
createElement(StateContexts.reflex___state____state__reflex___state____frontend_event_exception_state,{value: reflex___state____state__reflex___state____frontend_event_exception_state},
createElement(StateContexts.reflex___state____state__reflex___state____on_load_internal_state,{value: reflex___state____state__reflex___state____on_load_internal_state},
createElement(StateContexts.reflex___state____state__reflex___state____update_vars_internal_state,{value: reflex___state____state__reflex___state____update_vars_internal_state},
createElement(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state,{value: reflex___state____state__sandbox_reflex___state____auth_state},
createElement(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state,{value: reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state},
createElement(StateContexts.reflex___state____state__sandbox_reflex___state_form____form_state,{value: reflex___state____state__sandbox_reflex___state_form____form_state},
createElement(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state,{value: reflex___state____state__sandbox_reflex___state_hoteis____hotel_state},
createElement(StateContexts.reflex___state____state__sandbox_reflex___state_usuarios____usuario_state,{value: reflex___state____state__sandbox_reflex___state_usuarios____usuario_state},
    createElement(DispatchContext, {value: dispatchers}, children)
    ))))))))))
  )
}