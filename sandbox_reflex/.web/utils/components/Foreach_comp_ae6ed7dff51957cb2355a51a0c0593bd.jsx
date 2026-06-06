
import {Fragment,memo,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {Box as RadixThemesBox,Button as RadixThemesButton,Checkbox as RadixThemesCheckbox,Flex as RadixThemesFlex,Table as RadixThemesTable,Text as RadixThemesText} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Foreach_comp_ae6ed7dff51957cb2355a51a0c0593bd = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)
const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.registros_agrupados_rx_state_ ?? [],((row_rx_state_,index_09e2ea7e86951a866b0498c175d5c90f)=>(jsx(RadixThemesTable.Row,{key:index_09e2ea7e86951a866b0498c175d5c90f},jsx(RadixThemesTable.Cell,{},jsx(Fragment,{},(!((reflex___state____state__sandbox_reflex___state____auth_state.user_info_rx_state_?.["perfil"]?.valueOf?.() === "GESTOR"?.valueOf?.()))?(jsx(Fragment,{},jsx(RadixThemesText,{as:"label",size:"2"},jsx(RadixThemesFlex,{gap:"2"},jsx(RadixThemesCheckbox,{checked:reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.selected_records_rx_state_.includes(row_rx_state_?.["id"]),onCheckedChange:((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.toggle_record", ({ ["record_id"] : row_rx_state_?.["id"], ["is_checked"] : _ev_0 }), ({  })))], [_ev_0], ({  })))),size:"2"},),"")))):(jsx(Fragment,{},jsx(RadixThemesBox,{},)))))),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["data"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["caso"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["hotel"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["motivo"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["inicio"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["termino"]),jsx(RadixThemesTable.Cell,{},row_rx_state_?.["observacoes"]),jsx(RadixThemesTable.Cell,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"4"},jsx(RadixThemesButton,{css:({ ["fontSize"] : "1rem", ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_form____form_state.open_view_record", ({ ["record_id"] : row_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\ud83d\udc41\ufe0f"),jsx(Fragment,{},(!((reflex___state____state__sandbox_reflex___state____auth_state.user_info_rx_state_?.["perfil"]?.valueOf?.() === "GESTOR"?.valueOf?.()))?(jsx(Fragment,{},jsx(RadixThemesButton,{css:({ ["fontSize"] : "1rem", ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_form____form_state.open_edit_record", ({ ["record_id"] : row_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\u270f\ufe0f"))):(jsx(Fragment,{},jsx(RadixThemesBox,{},)))))))))))
    )
});
